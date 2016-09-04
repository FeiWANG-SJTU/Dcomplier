import d_lexer1
import d_parser
import d_ast1
import d_inte_gene_2bit_bus as d_inte_gene
import d_gene_v3 as d_gene
mypro=' for i = 1 : 1 i = i + 1 '

print('************************************')
print('user program:')
print()
print(mypro)
tokens=d_lexer1.d_lex(mypro)

root=d_ast1.tree('headers')
headers=d_parser.d_par(tokens)
print('************************************')

print('token stream :')
print()
for token in tokens:
    print(token)
    
for header in headers:
    #print(type(header),header.data)
    if header.id==1:
        root.add(header)
        #print(header)
#print(root.getchildren())
cod=d_inte_gene.in_gene(headers)
print('***********************************************')
print('intermediate code :')
print()
for co in cod:
    print(co.num,co.type ,co.in1 ,co.in2, co.in3 )          


ins=d_gene.d_gene(cod)



    

print()
print('***********************************************')
print('instructions:')
print()
for inn in ins:
    print(inn)
