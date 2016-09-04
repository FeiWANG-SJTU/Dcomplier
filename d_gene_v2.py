# function: generate machine code version 2
# 从中间代码产生机器码
# by OL , Sep 3, 2016
import re
#import simple_operations as sop
global poin
poin={'or':0,'and':4,'not':8,'xor':12}

def adder(inp1,inp2,oup1):
    global poin 
    tmp_table=[]
    # compiling of 1bit full adder
    if poin['xor']>14 or poin['and']>6: # pointer for and xor
        print( 'ERROR: SPACE not enough')
        return -1
    else :
        addr=[poin['xor'],oup1]
        poin['xor']+=1
        tmp_table.append([addr,[inp1,inp2],oup1])
        return tmp_table
    
def d_gene(incode):
    tmp_table=[]
    tmp_ins=[]# 暂存指令
    instr=[] #存放最终产生的指令
    idnum=len(incode)
    global poin
    #当前指针
    var=[] #暂时存放输出变量，直到最后要求输出那个再输出
    varpoi=0#变量指针序号
    numin=0 #输入变量的个数
    for i in range(10): #contain variables
        dic={'id':'','value':0}
        var.append(dic)
    #print(var)
    for cod in incode:
       
##        co=cod.split(': ')
##        print(co)
        co=cod.split()
        #print(co,len(co))
        if co[2]=='if':#对if语句的拆解
            tmp_ins.append(['FLAG',co[5],co[3]])
            
            
            inp=[co[3]]
            
            oup='[id,%s]'%idnum
            addr=[poin['not'],str(idnum)] #addr 用来建立输入与输出之间的联络，暂存于tmp_table
            poin['not']=poin['not']+1 #指针移动，无法判断是否走过了
            idnum=idnum+1
            tmp_table.append([addr, inp,oup])
            tmp_ins.append(['FLAG',co[8],oup])
        elif co[2]=='while': # 对while句的拆解
            addr=poin['whil']
        elif co[3]=='=': #赋值语句
            #print(co)
            addr=['var %d'%varpoi,co[0]]
            var[varpoi]['id']=co[2]
            var[varpoi]['value']=co[4]
            varpoi+=1
            inp=[co[2],co[4]]
            oup=co[0]
            tmp_table.append([addr, inp,oup])
        elif co[3] in ['==','!=','>','<','>=','<=']: # 关系运算
            inp1=co[2]
            inp2=co[4]
            oup=co[0]
            if co[3]=='==':
                tmp_table.extend(sop.neql(inp1,inp2,oup))
            elif co[3]=='!=':
                tmp_table.extend(sop.neql(inp1,inp2,oup))
            elif co[3]=='>':
                tmp_table.extend(sop.lthan(inp1,inp2,oup))
            elif co[3]=='<':
                tmp_table.extend(sop.sthan(inp1,inp2,oup))
            elif co[3]=='>=':
                tmp_table.extend(sop.nsthan(inp1,inp2,oup))
            elif co[3]=='<=':
                tmp_table.extend(sop.nlthan(inp1,inp2,oup))
  

        elif co[3] in ['+','-','*','/']: #算数运算
            inp1=co[2]
            inp2=co[4]
            oup=co[0]
            if co[3]=='+':
                tmp_table.extend(adder(inp1,inp2,oup))
            elif co[3]=='-':
                tmp_table.extend(suber(inp1,inp2,oup))
            elif co[3]=='*':
                tmp_table.extend(mul(inp1,inp2,oup))
            elif co[3]=='/':
                tmp_table.extend(div(inp1,inp2,oup))
        else :
            addr=[poin[co[3]],co[0]]
            poin[co[3]]=poin[co[3]]+1
            inp=[co[2],co[4]]
            oup=co[0]
            tmp_table.append([addr, inp,oup])
##    print(tmp_table)
##    print(var)
    #处理FLAG部分
    for ins in tmp_ins:
        if ins[0]=='FLAG':
            id1=(re.findall('[0-9]+',ins[1]))[0]
            id2=(re.findall('[0-9]+',ins[2]))[0]
            #print((id1))
            for tmp in tmp_table:
                oid1=tmp[0][1]
                
                if id1==oid1:
                    addr1=tmp[0][0]
                elif id2==oid1:
                    addr2=tmp[0][0]
        instr.append(['FLAG',addr1,addr2])
    #处理临时表
    print(tmp_table)
    for tmp in tmp_table:
        add2=tmp[0][0]
##        print((tmp))
##        print(instr)
        if isinstance(tmp[0][0],int):
            for i in range(len(tmp[1])):
                #print(tmp[1][i])
                
                if 'id' in tmp[1][i]: #输入中包含id的
                    add1=((re.findall('[0-9]+',tmp[1][i])))
                    #print(add1)
                    if not len(add1): #如果id后面是一个变量名
                        add1=numin
                        vname=(tmp[1][i].split(','))[1].split(']')[0]
                        toapp='INP(%s,%d)'%(vname,numin) #等待append
                        totest='INP(%s'%(vname)#等待判断是否已经输入
                        tmpf=0 #临时flag
                        for ins in instr:
                            if totest in ins:
                                tmpf=1
                        if not tmpf :
                            instr.append(toapp)
                        instr.append('WIR1(%d,%d,%d)'%(numin,add2,i))
                        numin=numin+1
                    else:
                        for ntmp in tmp_table:
                            oid1=ntmp[0][1]
                            if oid1==add1[0]:
                                instr.append('WIR2(%s,%s,%d)'%(ntmp[0][0],add2,i))
                                
                                break
                        
                elif 'num'in tmp[1][i]:
                    num=int((re.findall('[0-9]+',tmp[1][i]))[0])
                    instr.append('WIR1([num,%d],%s,%d)'%(num,add2,i))
                else :
                    print('error')
        vi=0
    #处理临时变量
    for va in var[0:varpoi]:
        vi+=1
       
        if 'id' in va['value']:
            vid=(va['value'].split(','))[1].split(']')[0]
            for tmp in tmp_table:
                oid1=tmp[0][1]
                if oid1==vid:
                    instr.append('VAR(%s,%s,%d)'%(va['id'].split(',')[1].split(']')[0],tmp[0][0],vi))
                    break
        else:
            instr.append('VAR(%s,%s,%d)'%(va['id'].split(',')[1].split(']')[0],va['value'],vi))
            
    
    print()
    return instr

#
# for testing
##cod=['2 :  [num,3] == [num,3]', '3 :  [id,b] = [num,3]',\
##     '5 :  [id,a] + [num,2]','4 :  [id,b] = [id,5]',\
##     '1 :  if [id,2] : [id,3] else : [id,4]']
cod=['5 :  [id,a] + [num,2]','4 :  [id,b] = [id,5]']
tabl=d_gene(cod)
for ta in tabl:
    print(ta)
