#function: change characters into tokens
# input: source program, 
# output: token stream
# by OL 2016.01.05
import sys
import re

RESV = 'RESERVED'
NUM = 'NUM'
ID = 'ID'

token_exprs= [
    (r'[ +]',None),#kong ge
    #(r'\s',None),
    (r'\n+', None), # huanhang
    (r'\t+',None), #zhi biao
    (r'#[^\n]*',None),# zhushi
    (r'==',RESV),
    (r'=',RESV),
    (r'\(',RESV),
    (r'\)',RESV),
    (r';',RESV),
    (r'\+',RESV),
    (r'-',RESV),
    (r'\*',RESV),
    (r'/',RESV),
    (r'<',RESV),
    (r'>',RESV),
    (r'>=',RESV),
    (r'<=',RESV),
    (r'!=',RESV),
    
    (r'and',RESV),
    (r'or',RESV),
    (r'xor',RESV),
    (r'not',RESV),
    (r'if',RESV),
    (r'else',RESV),
    (r'while',RESV),
    (r'for',RESV),
    (r'[0-9]',NUM),
    (r'[A-Za-z][A-Za-z0-9_ ]*',ID),
    ]  # all characters that can be recognized
def lex( characters, token_exprs):
    pos=0
    tokens=[]
    values =[] 
    while pos < len(characters):
        match = None
        for token_expr in token_exprs:
            pattern, tag=token_expr
            regex=re.compile(pattern)
            #print(dir(regex))
            match=regex.match(characters,pos)
            if match:
                text=match.group(0)
                if tag:
                    token=[text,tag]
                    
                    tokens.append(token)
                    if tag=='RESERVED':
                        values.append(text)
                    elif tag=='NUM':
                        values.append(tag)
                    elif tag== 'ID':
                        values.append(tag)
                    else:
                        values.append(text)
                 
                    break
        if not match:
            sys.stderr.write('Illegal character:%s\n' % characters[pos])
            sys.exit(1)
        else:
            pos=match.end(0)
    return tokens,values

def d_lex(characters):
    return lex(characters,token_exprs)
