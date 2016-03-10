#function: generate intermediate code
# imput : syntax tree
# output: intermediate code
# by OL , Jan.7, 2016
def in_gene(headers):
    cod=[]
    for header in headers:
        
        
        if header.data=='if': #如果是if节点
            a='%s : if [%s,%s] : [%s,%s] else : [%s,%s]'%(header.id,header.cchild[0].num,header.cchild[0].id,\
                                                       header.tchild[0].num,header.tchild[0].id,\
                                                      header.fchild[0].num, header.fchild[0].id)
            cod.append(a)
        elif header.data=='while': #while节点
            a='%s  :  while [%s,%s]:[%s,%s]'%(header.id,header.cchild[0].num,header.cchild[0].id,\
                                           header.bchild[0].num,header.bchild[0].id)
            cod.append(a)
        elif header.data =='=': #赋值运算
            a='%s  :  [%s,%s] = [%s,%s]'%(header.id,header.nchild[0].num,header.nchild[0].id,\
                                       header.achild[0].num,header.achild[0].id)
            cod.append(a)
        elif header.data in ['==','!=','<=','>=','<','>']: #关系运算
            a='%s  :  [%s,%s] %s [%s,%s]'%(header.id,header.lchild[0].num,header.lchild[0].id,\
                                       header.data,header.rchild[0].num,header.rchild[0].id)
            cod.append(a)
        elif header.data in ['and','or','xor','not']:#逻辑运算
            a='%s  :  [%s,%s] %s [%s,%s]'%(header.id,header.lchild[0].num,header.lchild[0].id,\
                                        header.data , header.rchild[0].num,header.rchild[0].id)
            cod.append(a)
        elif header.data in ['+','-']: #
            a='%s  :  [%s,%s] %s [%s,%s]'%(header.id,header.tchild[0].num,header.tchild[0].id,\
                                        header.data,header.fchild[0].num,header.fchild[0].id)
            cod.append(a)
        elif header.data in ['*','/']:
            a='%s  :  [%s,%s] %s [%s,%s]'%(header.id,header.fchild[0].num,header.fchild[0].id,\
                                        header.data,header.tchild[0].num,header.tchild[0].id)
            cod.append(a)
    return cod          


