# function: generate machine code version 2
# 从中间代码产生机器码
# by OL , Sep 3, 2016
import re
import math
from d_inte_gene_2bit_bus import incd
#import simple_operations as sop
global poin
poin={'or':1000,'and':1004,'not':1008,'xor':1012}

##def adder(inp1,inp2,oup1):
##    
##    global poin 
##    tmp_table=[]
##    # compiling of 1bit full adder
##    if poin['xor']>14 or poin['and']>6: # pointer for and xor
##        print( 'ERROR: SPACE not enough')
##        return -1
##    else :
##        addr=[poin['xor'],oup1]
##        poin['xor']+=1
##        tmp_table.append([addr,[inp1,inp2],oup1])
##        return tmp_table
def adder(inp1,inp2,oup):
    #2bit inp1[0] inp1[1] inp2[0] inp2[1]
    # out: oup[0] oup[1]
    global poin 
    tmp_table=[]
    # compiling of 1bit full adder
    if poin['xor']>1013 or poin['and']>1006: # pointer for and xor
        #print(poin['xor'],poin['and'])
        print( 'ERROR: SPACE not enough')
        return -1
    else :
        addr=[['id',poin['xor']],oup[0]]
        tmp_table.append([addr,[inp1[0],inp2[0]],oup[0]])
        poin['xor']+=1
        addr=[['id',poin['and']],poin['xor']+1]
        tmp_table.append([addr,[inp1[0],inp2[0]],poin['xor']+1])
        poin['and']+=1
        addr=[['id',poin['xor']],poin['xor']+1]
        tmp_table.append([addr,[inp1[1],inp2[1]],poin['xor']+1])
        poin['xor']+=1
        addr=[['id',poin['xor']],oup[1]]
        tmp_table.append([addr,[['id',poin['xor']-1],['id',poin['and']-1]],oup[1]])
        poin['xor']+=1
##        for tmp in tmp_table:
##            print(tmp)
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

    #############
    ##把每一句拆成2bit格式的    
    nincode=[] # new generated code
    for cod in incode:
        ncod=incd()
        ncod.num=[cod.num*2-1,cod.num*2]
        ncod.type=cod.type
        if not cod.in1:
            ncod.in1=[]
        elif cod.in1[0]=='id':
            if type(cod.in1[1])== int:
                ncod.in1=[[cod.in1[0],cod.in1[1]*2-1],[cod.in1[0],cod.in1[1]*2]]
            else:
                ncod.in1=[[cod.in1[0],cod.in1[1]+'_0'],[cod.in1[0],cod.in1[1]+'_1']]
        elif cod.in1[0]=='num':
            b0=int(cod.in1[1])%2
            b1=math.floor (int(cod.in1[1])/2)
            ncod.in1=[['num',b0],['num',b1]]
        else:
            ncod.in1=[]
        if not cod.in2:
            ncod.in2=[]   
        elif cod.in2[0]=='id':
            if type(cod.in2[1])== int:
                ncod.in2=[[cod.in2[0],cod.in2[1]*2-1],[cod.in2[0],cod.in2[1]*2]]
            else:
                ncod.in2=[[cod.in2[0],cod.in2[1]+'_0'],[cod.in2[0],cod.in2[1]+'_1']]
        elif cod.in2[0]=='num':
            b0=int(cod.in2[1])%2
            b1=math.floor (int(cod.in2[1])/2)
            ncod.in2=[['num',b0],['num',b1]]
        else:
            ncod.in2=[]

        if not cod.in3:
            ncod.in3=[]
        elif cod.in3[0]=='id':
            if type(cod.in3[1])== int:
                ncod.in3=[[cod.in3[0],cod.in3[1]*2-1],[cod.in3[0],cod.in3[1]*2]]
            else:
                ncod.in3=[[cod.in3[0],cod.in3[1]+'_0'],[cod.in3[0],cod.in3[1]+'_1']]
        elif cod.in3[0]=='num':
            b0=int(cod.in3[1])%2
            b1=math.floor (int(cod.in3[1])/2)
            ncod.in3=[['num',b0],['num',b1]]
        else:
            ncod.in3=[]
        nincode.append(ncod)
        #print(ncod.num,ncod.type ,ncod.in1 ,ncod.in2, ncod.in3 )
##    for co in nincode:
##        print(co.num,co.type ,co.in1 ,co.in2, co.in3 ) 
    ######拆分结束
    ####对新的incode进行分析
    for co in nincode:
        #print(co,len(co))
        if co.type=='if':#对if语句的拆解
            tmp_ins.append(['FLAG',co.in2[0],co.in1[0]])
            
            
            inp=[co.in1[0]]
            
            oup='[id,%d]'%idnum
            addr=[poin['not'],str(idnum)] #addr 用来建立输入与输出之间的联络，暂存于tmp_table
            poin['not']=poin['not']+1 #指针移动，无法判断是否走过了
            idnum=idnum+1
            tmp_table.append([addr, inp,oup])
            tmp_ins.append(['FLAG',co.in3[0],oup])
        elif co.type=='while': # 对while句的拆解
            addr=poin['whil']
        elif co.type=='=': #赋值语句
            #print(co)
            addr=['var %d'%varpoi,co.num[0]]
            var[varpoi]['id']=co.in1[0]
            var[varpoi]['value']=co.in2[0]
            varpoi+=1
            inp=[co.in2[0]]
            oup=co.num[0]
            tmp_table.append([addr, inp,oup])
            addr=['var %d'%varpoi,co.num[1]]
            var[varpoi]['id']=co.in1[1]
            var[varpoi]['value']=co.in2[1]
            varpoi+=1
            inp=[co.in2[1]]
            oup=co.num[1]
            tmp_table.append([addr, inp,oup])
        elif co.type in ['==','!=','>','<','>=','<=']: # 关系运算
            # not finished
            inp1=co.in1
            inp2=co.in2
            oup=num
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
  

        elif co.type in ['+','-','*','/']: #算数运算
            inp1=co.in1
            inp2=co.in2
            oup=co.num
            if co.type=='+':
                
                tmp_table.extend(adder(inp1,inp2,oup))
            elif co[3]=='-':
                tmp_table.extend(suber(inp1,inp2,oup))
            elif co[3]=='*':
                tmp_table.extend(mul(inp1,inp2,oup))
            elif co[3]=='/':
                tmp_table.extend(div(inp1,inp2,oup))
##        else :
##            addr=[poin[co[3]],co[0]]
##            poin[co[3]]=poin[co[3]]+1
##            inp=[co[2],co[4]]
##            oup=co[0]
##            tmp_table.append([addr, inp,oup])
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
    print('tmp table')
    for tmp in tmp_table:
        print(tmp)
    for tmp in tmp_table:
        add2=tmp[0][0][1]
        #print((tmp))
##        print(instr)
##        if isinstance(tmp[0][0],int):
        for i in range(len(tmp[1])):
            #两个input
##            print('****')
##            print(tmp[1][i])
            if 'id' in tmp[1][i]: #输入中包含id的
                add1=tmp[1][i][1]
                #print('add1',add1)
                if type(add1)==str:
                    #如果id后面是一个变量名,表示需要输入input
                    add1=numin
                    vname=tmp[1][i][1]
                    toapp='INP(%s,%d)'%(vname,numin) #等待append
                    totest='INP(%s'%(vname)#等待判断是否已经输入
                    tmpf=0 #临时flag
                    lo=0 #所在位置
                    for ins in instr:
                        if totest in ins:
                            tmpf=1
                            break
                        else:
                            lo+=1
                    if not tmpf :
                        instr.append(toapp)
                        instr.append('WIR1(%d,%s,%d)'%(numin,add2,i))
                        numin=numin+1
                    else:
                        #如果变量表中已经有这个变量了。
                        instr.append('WIR1(%d,%s,%d)'%(lo,add2,i))
                    
                    
                else:
                    #在临时表中寻找输出的位置
                    for ntmp in tmp_table:
                        oid1=ntmp[0][0][1]
                        #print(oid1,add1)
                        if oid1==add1:
                            instr.append('WIR2(%s,%s,%d)'%(ntmp[0][0][1],add2,i))
                            #print('WIR2(%s,%s,%d)'%(ntmp[0][0],add2,i))
                            break
                    
            elif 'num'in tmp[1][i]:
                num=tmp[1][i][1]
                instr.append('WIR1([num,%d],%s,%d)'%(num,add2,i))
            else :
                print('error')
##            print(tmp)
##            print(instr)
        vi=0
    #处理临时变量
    for va in var[0:varpoi]:
        vi+=1
##        print('***************')
##        print(va)
        if 'id' in va['value']:
            vid=va['value'][1]
            for tmp in tmp_table:
                oid1=tmp[0][1]
                if oid1==vid:
                    instr.append('VAR(%s,%s,%d)'%(va['id'][1],tmp[0][0][1],vi))
                    break
        else:
            instr.append('VAR(%s,%s,%d)'%(va['id'][1],va['value'][1],vi))
            
    
    print()
    return instr

###
### for testing
####cod=['2 :  [num,3] == [num,3]', '3 :  [id,b] = [num,3]',\
####     '5 :  [id,a] + [num,2]','4 :  [id,b] = [id,5]',\
####     '1 :  if [id,2] : [id,3] else : [id,4]']
##cod=['5 :  [id,a] + [num,2]']
##tabl=d_gene(cod)
##for ta in tabl:
##    print(ta)
