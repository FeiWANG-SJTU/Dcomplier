class node:
 
    def __init__(self, values):
        self.values = values
        self.children = []
        self.tokens 
 
    def getdata(self):
        return self.data
 
    def getchildren(self):
        return self._children
 
    def add(self, node):
        ##if full
        if len(self._children) == 4:
            return False
        else:
            self._children.append(node)
 
    def go(self, data):# visit child, if contain data
        for child in self._children:
            if child.getdata() == data:
                return child
        return None
 
class tree:
 
    def __init__(self,data):
        self._head = node(data)
 
    def linktohead(self, node):
        self._head.add(node)
 
    def insert(self, path, data):
        cur = self._head
        for step in path:
            if cur.go(step) == None:
                return False
            else:
                cur = cur.go(step)
        cur.add(node(data))
        return True
class ifstmt():
    def __init__ (self,values):
        self.values=values #创建一个节点
        self.tokens=[]
        self.values=[]
    def addtoken(self,tokens):
        self.tokens.append(tokens)
    def addvalues(self,values):
        self.values.append(values)
    def createxpr():
        self._head.add(
        

    
class AssignStmt():
    def __init__(self, name, aexp):
        self.name = name
        self.aexp = aexp
        
#condition statement
class If():
    def __init__(self, condition, true_stmt,false_stmt):
        self.condition=condition
        self.true_stmt=true_stmt
        self.false_stmt=false_stmt
    def eval(self, env):  ##????
        condition_value = self.condition.eval(env)
        if condition_value:
            self.true_stmt.eval(env)
        else:
            if self.false_stmt:
                self.false_stmt.eval(env)
class Whil():
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __repr__(self):
        return 'WhileStatement(%s, %s)' % (self.condition, self.body)
class WhileStatement(Statement):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __repr__(self):
        return 'WhileStatement(%s, %s)' % (self.condition, self.body)

    def eval(self, env):
        condition_value = self.condition.eval(env)
        while condition_value:
            self.body.eval(env)
            condition_value = self.condition.eval(env)
#logical operation
class RelOp():

class AndOp():

class OrOp():

class XorOp():

