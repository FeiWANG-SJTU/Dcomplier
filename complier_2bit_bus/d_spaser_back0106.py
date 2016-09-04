import d_ast1

def ifif(tokens):#如果是if语句，则创建if节点
    print(tokens)
    for token in tokens:
        if ':' in token:
            cpos=tokens.index (token)
        if 'else' in token:
            elpos=tokens.index (token)
            break
    condition=tokens[1:cpos]
    true_stmt=tokens[cpos+1:elpos]
    false_stmt=tokens[elpos+2:len(tokens)]
    print('true',true_stmt)
    print('false',false_stmt)
    nheader=d_ast1.If(condition, true_stmt,false_stmt)
    return nheader
def ifwhil(tokens):
    print(tokens)
    cpos=0
    op=tokens[0][0]
    for token in tokens:
        if ':' in token:
            cpos=tokens.index(token)
            break
    condition=tokens[1:cpos]
    body=tokens[cpos+1:len(tokens)]
    nheader=d_ast1.Whil(condition, body)
    return nheader
def ifrel(tokens):
    print(tokens)
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
    print(tokens)
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
    print(tokens)
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
    print(tokens)
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
    print(tokens)
    name=tokens[0]
    aexp=tokens[2:len(tokens)]
    nheader=d_ast1.AssignStmt(name, aexp)
    return nheader
def isif(tokens):
    if token[0][0]=='if':
        return True
    else :
        return False
def iswhil(tokens):
    if token[0][0]=='while':
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
    #print(header.name)
    if isrel(header.condition):
        nheader=ifrel(header.condition)
        header.addcchild(nheader)
        visitrel(nheader)
    # 进入并执行新建的节点
    elif islog (header.condition):
        nheader=iflog(header.condition)
        header.addcchild(nheader)
        visitlog(nheader)
    else:
        header.addcchild(d_ast1.node(header.condition))# 需要修改NODE class
    print(header.false_stmt)    
    if isassign(header.true_stmt): #执行语句只有赋值语句
        nheader=ifassign(header.true_stmt)
        header.addtchild(nheader)
        visitassign(nheader)
    else:
        print('error ')
    if isassign(header.false_stmt):
        nheader=ifassign(header.false_stmt)
        header.addfchild(nheader)
        visitassign(nheader)
    else:
        print('error ')
    return header
def visitwhil(header):
    #print(header.name)
    if isrel(header.codition):
        nheader=ifrel(header.condition)
        header.addcchild(nheader)
        visitrel(nheader)
    # 进入并执行新建的节点
    elif islog (header.condition):
        nheader=iflog(header.condition)
        header.addcchild(nheader)
        visitlog(nheader)
    else:
        header.addcchild(d_ast1.node(header.condition))# 需要修改NODE class
        
    if isassign(header.body): #执行语句只有赋值语句
        nheader=iflog(header.body)
        header.addbchild(nheader)
        visitassign(nheader)
    else:
        print('error ')
    return header
def visitassign(header):
    #print(header.name)
    header.addnchild(d_ast1.node(header.name))
    if len(header.aexp)==1:
        header.addachild(d_ast1.node(header.aexp))
    elif isrel(header.aexp):
        print(header.aexp)
        nheader=ifrel(header.aexp)
        header.addachild(nheader)
        visitrel(nheader)
    # 进入并执行新建的节点
    elif islog (header.aexp):
        nheader=iflog(header.aexp)
        header.addachild(nheader)
        visitlog(nheader)
    else:
        nheader=ifterm(header.aexp)
        header.addachild(nheader)
        visitterm(nheader)
    return header 
def visitrel(header):
    #print(header.name)

    # 进入并执行新建的节点
    if islog (header.rel1):
        nheader=iflog(header.rel1)
        header.addlchild(nheader)
        visitlog(nheader)
    elif isterm(header.rel1):
        nheader=ifterm(header.rel1)
        header.addlchild(nheader)
        visitterm(nheader)
    else:
        header.addrchild(d_ast1.node(header.rel1))# 需要修改NODE class
                  
    
    # 进入并执行新建的节点
    if islog (header.rel2):
        nheader=iflog(header.rel2)
        header.addrchild(nheader)
        visitlog(nheader)
    elif isterm(header.rel2):
        nheader=ifterm(header.rel2)
        header.addrchild(nheader)
        visitterm(nheader)
    else:
        header.addrchild(d_ast1.node(header.rel2))# 需要修改NODE class
    return header

def visitterm(header):
    
    if isterm(header.term):
        nheader=ifterm(header.term)
        header.addtchild(nheader)
        visitterm(nheader)
    # 进入并执行新建的节点
    else:
        nheader=iffactor(header.term)
        header.addtchild(nheader)
        visitfactor(nheader)
        
    nheader=iffactor(header.factor)
    header.addfchild(nheader)
    visitfactor(nheader)
    return header
def visitfactor(header):
    #print(header.name)
    if isfactor(header.factor):
        nheader=ifterm(header.factor)
        header.addfchild(nheader)
        visitfactor(nheader)
    # 进入并执行新建的节点
    else:
        header.addfchild(node(header.factor))
    header.addtchild(d_ast1.node(header.ter))
    return header

              
headers=[]     
tokens=[['if', 'reserved'], ['id', 'b'], ['==', 'reserved'], ['num', '3'], \
 ['id', ':'], ['id', 'a'], ['=', 'reserved'], ['num', '5'], ['else', 'reserved'], ['id', ':'], \
 ['id', 'a'], ['=', 'reserved'], ['num', '3']]
nheader=ifif(tokens)
#print(nheader.data)
visitif(nheader)    
            
