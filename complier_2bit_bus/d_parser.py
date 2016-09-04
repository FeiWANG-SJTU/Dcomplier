#function : construct syntax tree from tokens
# input: token list
# output: syntaxtree
# by OL Jan.7, 2016
import d_ast1
headers=[]
idnum=0
#建立对应的节点
def ifif(tokens):#如果是if语句，则创建if节点
    #print(tokens)
    for token in tokens:
        if ':' in token:
            cpos=tokens.index (token)
        if 'else' in token:
            elpos=tokens.index (token)
            break
    condition=tokens[1:cpos]
    true_stmt=tokens[cpos+1:elpos]
    false_stmt=tokens[elpos+2:len(tokens)]
    #print('true',true_stmt)
    #print('false',false_stmt)
    nheader=d_ast1.If(condition, true_stmt,false_stmt)
    return nheader
def iffor (tokens):
    condition_vari=tokens[1][0]
    strt=int(tokens[3][1])
    stp=int(tokens[5][1])
    body=tokens[6:]
    #print(type(stp))
    nheader=d_ast1.For(strt, stp, condition_vari, body)
    return nheader
def ifwhil(tokens):
    #print(tokens)
    cpos=0
    op=tokens[0][0]
    for token in tokens:
        if ':' in token:
            cpos=tokens.index(token)
            break
    condition=tokens[1:cpos]
    
    body=tokens[cpos+1:len(tokens)]
    
    nheader=d_ast1.Whil(condition, body)
    print(nheader)
    return nheader
def ifrel(tokens):
    #print(tokens)
    cpos=0
    op=tokens[0][0]
    for token in tokens:
        if token[0] in ['==','!=','<=','>=','<','>']:
            cpos=tokens.index(token)
            op=token[0]
            break
    expr1=tokens[0:cpos]
    expr2=tokens[cpos+1:len(tokens)]
    nheader=d_ast1.Rel(expr1,expr2,op)
    return nheader

def iflog(tokens):
    #print(tokens)
    cpos=0
    op=tokens[0][0]
    for token in tokens:
        if token[0] in ['and','or','xor','not']:
            cpos=tokens.index(token)
            op=token[0]
            
            break
    expr1=tokens[0:cpos]
    expr2=tokens[cpos+1:len(tokens)]
    nheader=d_ast1.Log(expr1,expr2,op)
    return nheader

def ifterm(tokens):
    #print(tokens)
    #(tokens)
    cpos=0
    op=tokens[0][0]
    for token in tokens:
        if token[0] in['+','-']:
            cpos=tokens.index(token)
            op=token[0]
            break
    expr1=tokens[0:cpos]
    expr2=tokens[cpos+1:len(tokens)]
    nheader=d_ast1.Term(expr1,expr2,op)
    return nheader

def iffactor(tokens):
    #print(tokens)
    cpos=0
    op=tokens[0][0]
    for token in tokens:
        if token[0] in['*','/']:
            cpos=tokens.index(token)
            op=token[0]
            break
    expr1=tokens[0:cpos]
    expr2=tokens[cpos+1:len(tokens)]
    nheader=d_ast1.Factor(expr1,expr2,op)
    return nheader
def ifassign(tokens):
    #print(tokens)
    name=tokens[0]
    aexp=tokens[2:len(tokens)]
    nheader=d_ast1.AssignStmt(name, aexp)
    return nheader

##以下判断一个tokens list属于哪种表达
def isif(tokens):
    if tokens[0][0]=='if':
        return True
    else :
        return False
def iswhil(tokens):
    if tokens[0][0]=='while':
        return True
    else :
        return False
def isfor(tokens):
    if tokens[0][0]=='for':
        return True
    else :
        return False
def isrel(tokens):
    for token in tokens:
        if token[0] in ['==','!=','<=','>=','<','>']:
            return True
    return False
def islog(tokens):
    for token in tokens:
        if token[0] in ['and','or','xor','not']:
            return True
        else:
            return False
def isassign(tokens):
    if tokens[1][0]=='=':
        return True
    else:
        return False
def isterm(tokens):
    for token in tokens:
        if token[0] in['+','-']:
            return True
        else:
            return False
def isfactor(tokens):
    for token in tokens:
        if token[0] in['*','/']:
            return True
        else:
            return False
    
### 开始visit
def visitif(header):
    global headers
    global idnum
    idnum+=1
    header.id=idnum
    #print(type(header))
    
    #print(header.name)
    if isrel(header.condition):
        nheader=ifrel(header.condition)
        header.addcchild(nheader)
        
        visitrel(nheader)
        headers.append(nheader)
    # 进入并执行新建的节点
    elif islog (header.condition):
        nheader=iflog(header.condition)
        header.addcchild(nheader)
        
        visitlog(nheader)
        
        headers.append(nheader)
    else:
        header.addcchild(d_ast1.node(header.condition))# 需要修改NODE class
        
    #print(header.false_stmt)    
    if isassign(header.true_stmt): #执行语句只有赋值语句
        nheader=ifassign(header.true_stmt)
        header.addtchild(nheader)
        
        visitassign(nheader)
        headers.append(nheader)
    else:
        print('error ')
    #print(isassign(header.false_stmt))
    if isassign(header.false_stmt):
        nheader=ifassign(header.false_stmt)
        header.addfchild(nheader)
        
        visitassign(nheader)
        headers.append(nheader)
    else:
        print('error ')
    #headers.append(header)
    return header

def visitfor(header):
    global headers
    global idnum
    idnum+=1
    header.id=idnum
    #print(type(header))
    
    if isassign(header.body): #执行语句只有一句赋值语句
        for i in range(header.strt,header.stp+1):
            tmp=header.body
            nheader=ifassign(header.body)
            header.addchild(nheader)
            visitassign(nheader)
            headers.append(nheader)
    else:
        print('not supported expression')

def visitwhil(header):
    #print(type(header))
    global headers
    global idnum
    idnum+=1
    header.id=idnum
    #print(header.name)
    if isrel(header.condition):
        nheader=ifrel(header.condition)
        header.addcchild(nheader)
        
        visitrel(nheader)
        headers.append(nheader)
    # 进入并执行新建的节点
    elif islog (header.condition):
        nheader=iflog(header.condition)
        header.addcchild(nheader)
        
        visitlog(nheader)
        headers.append(nheader)
    else:
        header.addcchild(d_ast1.node(header.condition))# 需要修改NODE class
        
        
    if isassign(header.body): #执行语句只有赋值语句
        nheader=ifassign(header.body)
        header.addbchild(nheader)
        
        visitassign(nheader)
        headers.append(nheader)
    else:
        print('error ')
    #headers.append(header)
    return header
def visitassign(header):
    #print(type(header))
    global headers
    global idnum
    idnum+=1
    header.id=idnum

    #print(header.name)
    header.addnchild(d_ast1.node([header.name]))
    if len(header.aexp)==1:
        header.addachild(d_ast1.node(header.aexp))
    elif isrel(header.aexp):
        print(header.aexp)
        nheader=ifrel(header.aexp)
        header.addachild(nheader)
        visitrel(nheader)
        headers.append(nheader)
    # 进入并执行新建的节点
    elif islog (header.aexp):
        nheader=iflog(header.aexp)
        header.addachild(nheader)
        visitlog(nheader)
        headers.append(nheader)
    else:
        nheader=ifterm(header.aexp)
        header.addachild(nheader)
        visitterm(nheader)
        headers.append(nheader)
    #headers.append(header)
    return header 
def visitrel(header):
    #print(type(header))
    global headers
    global idnum
    #print(header.name)
    idnum+=1
    header.id=idnum


    # 进入并执行新建的节点
    if islog (header.rel1):
        nheader=iflog(header.rel1)
        header.addlchild(nheader)
        visitlog(nheader)
        headers.append(nheader)
    elif isterm(header.rel1):
        nheader=ifterm(header.rel1)
        header.addlchild(nheader)
        visitterm(nheader)
        headers.append(nheader)
    else:
        header.addlchild(d_ast1.node(header.rel1))# 需要修改NODE class
                  
    
    # 进入并执行新建的节点
    if islog (header.rel2):
        nheader=iflog(header.rel2)
        header.addrchild(nheader)
        visitlog(nheader)
        headers.append(nheader)
    elif isterm(header.rel2):
        nheader=ifterm(header.rel2)
        header.addrchild(nheader)
        visitterm(nheader)
        headers.append(nheader)
    else:
        header.addrchild(d_ast1.node(header.rel2))# 需要修改NODE class
    
    return header

def visitterm(header):
    #print(type(header))
    global headers
    global idnum
    idnum+=1
    header.id=idnum
    
    if isterm(header.term):
        nheader=ifterm(header.term)
        header.addtchild(nheader)
        visitterm(nheader)
        headers.append(nheader)
    # 进入并执行新建的节点
    elif isfactor(header.term):
        nheader=iffactor(header.term)
        header.addtchild(nheader)
        visitfactor(nheader)
        headers.append(nheader)
    else:
        header.addtchild(d_ast1.node(header.term))

    if isfactor(header.factor):
        nheader=iffactor(header.factor)
        header.addfchild(nheader)
        visitfactor(nheader)
        headers.append(nheader)
    else:
        header.addfchild(d_ast1.node(header.factor))
    return header
def visitfactor(header):
    #print(type(header))
    global headers
    global idnum
    idnum+=1
    header.id=idnum
    #print(header.name)
    if isfactor(header.factor):
        nheader=ifterm(header.factor)
        header.addfchild(nheader)
        visitfactor(nheader)
        headers.append(nheader)
    # 进入并执行新建的节点
    else:
        header.addfchild(d_ast1.node(header.factor))
    header.addtchild(d_ast1.node(header.ter))
    #headers.append(header)
    return header

def d_par(tokens):
    #开始执行，调用上述函数
    global headers
    global idnum
    root=d_ast1.tree('headers')
##    import pdb
##    pdb.set_trace()
    if isif(tokens):
        nheader=ifif(tokens)
        root.add(nheader)
        visitif(nheader)
        headers.append(nheader)
    elif isfor(tokens):
        nheader=iffor(tokens)
        root.add(nheader)
        visitfor(nheader)
        headers.append(nheader)
    elif iswhil(tokens):
        nheader=ifwhil(tokens)
        root.add(nheader)
        visitwhil(nheader)
        headers.append(nheader)
    elif isassign(tokens): #执行语句只有赋值语句
        nheader=ifassign(tokens)
        header.addbchild(nheader)
        root.add(nheader)
        visitassign(nheader)
        headers.append(nheader)
    elif isrel(tokens):
        nheader=ifrel(tokens)
        root.add(nheader)
        visitrel(nheader)
        headers.append(nheader)
    elif islog (tokens):
        nheader=iflog(tokens)
        root.add(nheader)
        visitlog(nheader)
        headers.append(nheader)
    elif isterm(tokens):
        nheader=ifterm(tokens)
        root.add(nheader)
        visitterm(nheader)
        headers.append(nheader)
    elif isfactor(tokens):
        nheader=ifterm(tokens)
        root.add(nheader)
        visitfactor(nheader)
        headers.append(nheader)
    
    return headers

#for testing code
##headers=[]
##idnum=0
##root=d_ast1.node(headers)
##tokens=[['if', 'reserved'], ['id', 'b'], ['==', 'reserved'], ['num', '3'], \
## ['id', ':'], ['id', 'a'], ['=', 'reserved'], ['num', '5'], ['else', 'reserved'], ['id', ':'], \
## ['id', 'a'], ['=', 'reserved'], ['num', '3']]
###nheader=ifif(tokens)
###print(nheader.data)
###visitif(nheader)
##strt(tokens)
##print(len(headers))
##for header in headers:
##    print(header.id)



    
