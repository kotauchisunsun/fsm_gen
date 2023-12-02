from parsy import regex,string,decimal_digit,seq,whitespace,generate,success

class Atom:
    def __init__(self,type,value):
        self.type = type
        self.value = value

    def __str__(self):
        return f"(TYPE={self.type} VALUE={self.value})"

    def __repr__(self):
        return str(self)

class Op:
    def __init__(self,name):
        self.name = name

    def __repr__(self):
        return f"(OP NAME={self.name})"

class Term:
    def __init__(self,op,x,y):
        self.op = op
        self.x = x
        self.y = y

    def __repr__(self):
        return f"(TERM OP={self.op} X={self.x} Y={self.y})"

class Decl:
    def __init__(self,type,var,value):
        self.type = type
        self.var = var
        self.value = value

    def __repr__(self):
        return f"(DECL TYPE={self.type} NAME={self.var} VALUE={self.value})"

class Assign:
    def __init__(self,var,value):
        self.var = var
        self.value = value
        
    def __repr__(self):
        return f"(ASSIGN VAR={self.var} VALUE={self.value})"

class Var:
    def __init__(self,name):
        self.name = name

    def __repr__(self):
        return f"(VAR NAME={self.name})"

class Label:
    def __init__(self,name):
        self.name = name

    def __repr__(self):
        return f"(LABEL NAME={self.name})"

class Goto:
    def __init__(self,name):
        self.name = name

    def __repr__(self):
        return f"(GOTO NAME={self.name})"

class Block:
    def __init__(self,statements):
        self.statements = statements

    def __repr__(self):
        def _():
            yield "(BLK START)"
            for s in self.statements:
                yield str(s)
            yield "(BLK END)"

        return "\n".join(_())

class If:
    def __init__(self,logic,block):
        self.logic = logic
        self.block = block

    def __repr__(self):
        def _():
            yield f"(IF (LOGIC={self.logic}))"
            yield str(self.block)
            yield "(ENDIF)"
        return "\n".join(_())

class Print:
    def __init__(self,format,*args):
        self.format = format
        self.args = args
    
    def __repr__(self):
        def _():
            yield f"(PRINT FORMAT={self.format}"
            for a in self.args:
                yield " "+str(a)
            yield ")"
        return "".join(_())

class Logic:
    def __init__(self,op,a,b):
        self.op = op
        self.a = a
        self.b = b

    def __repr__(self):
        return f"(LOGIC OP='{self.op}' A={self.a} B={self.b})"

var = regex("[a-zA-Z_]+[a-zA-Z0-9]*").map(lambda x:Var(x))
digit = regex(r'[-+]?[1-9]*[0-9]').map( lambda x: Atom("INT",x))
str_data = (string('"') >> regex(r'[0-9_a-zA-Z{}\[\](),. %=]*') << string('"')).map( lambda x:Atom("STR",x))

_ = regex("[_\s]*")

atom = digit | var

factor_op = string("*").map(lambda x:Op("MUL")) | string("/").map(lambda x:Op("DIV"))
term_op = string("+").map(lambda x:Op("ADD")) | string("-").map(lambda x:Op("SUB"))

@generate
def multiplicative():
    res = yield term
    while True:
        yield _
        operation = yield factor_op | success("")
        if not operation:
            break
        yield _
        operand = yield term
        res = Term(operation,res,operand)
    return res

@generate
def additive():
    res = yield multiplicative
    while True:
        yield _
        operation = yield term_op | success("")
        if not operation:
            break
        yield _
        operand = yield multiplicative
        res = Term(operation,res,operand)
    return res

lp = string("(")
rp = string(")")

expr = additive
term = (lp >> expr << rp) | atom

w = regex("[ ]+")

assign_op = string("=")
int_type = string("int")
string_type = string("str")

label_statement = (string("label:")>>w>>var).map(lambda x:Label(x.name))
int_decl_statement = seq(int_type >> w >> var << w,string("=")<<w,expr).map(lambda x:Decl("INT",x[0],x[2]))
str_decl_statement = seq(string_type >> w >> var << w,string("=")<<w,str_data).map(lambda x:Decl("STR",x[0],x[2]))
assign_statement = seq(var <<w,string("=")<<w,expr).map(lambda x:Assign(x[0],x[2]))
goto_statement = (string("goto")>>w>>var).map(lambda x:Goto(x.name))
#print_statment = seq(string("print") >> w >> str_data,(w >> var).many()).map(lambda x:Print(x[0],*x[1]))
print_statment = seq(string("print") >> w >> str_data,(w >> var).many()).map(lambda x:Print(x[0],*x[1]))
#print_statment = string("print") >> w >> str_data

decl_statement = int_decl_statement | str_decl_statement


logic_op = string(">") | string("==")
logic_statement = seq(expr,_>>logic_op<<_,expr).map(lambda x:Logic(x[1],x[0],x[2]))



blank_line = regex("[\s\n]*")

lbrace = string("{")
rbrace = string("}")

@generate
def statement():
    return (yield if_block | decl_statement | assign_statement | label_statement | goto_statement | print_statment)

@generate
def line():
    return (yield _ >> statement << _ << regex("\n*"))

@generate
def block():
    return ( yield seq(lbrace>>blank_line>>line.many()<<blank_line<<rbrace).map(lambda x:Block(x[0])))

@generate
def if_block():
    return (yield seq(string("if")>>_>>lp>>_>>logic_statement,_>>rp>>_>>block).map(lambda x:If(x[0],x[1])))

program = block
parser = expr

from asm import *
from util import get_random_name

result = "result_register"

def compile(ast):
    if type(ast)==Decl:
        decl = ast
        if decl.type=="INT":
            for a in compile(decl.value):
                yield a
            yield (INT,decl.var.name,0)
            yield (LDI,decl.var.name,result)
        elif decl.type=="STR":
            yield (STR,decl.var.name,decl.value.value)
    elif type(ast)==Atom:
        tmp = get_random_name("atom")
        if ast.type=="INT":
            yield (INT,tmp,int(ast.value))
            yield (LDI,result,tmp)
    elif type(ast)==Assign:
        assign = ast
        for a in compile(assign.value):
            yield a
        yield (LDI,assign.var.name,result)
    elif type(ast)==Label:
        label = ast
        yield (label.name,LDI,result,result)
    elif type(ast)==Goto:
        label = ast
        tmp = get_random_name("atom")
        yield (INT,tmp,0)
        yield (JZE,tmp,label.name)    
    elif type(ast)==If:
        if_op = ast
        skip_label = get_random_name("skip")
        for a in compile(if_op.logic):
            yield a
        yield (JZE,result,skip_label)
        yield (JMI,result,skip_label)
        for a in compile(if_op.block):
            yield a
        yield (skip_label,LDI,result,result)
    elif type(ast)==Print:
        print_op = ast
        tmp = get_random_name("fmt")
        yield (STR,tmp,"")
        yield (FMS,tmp,print_op.format.value,*[a.name for a in print_op.args])
        yield (PRT,tmp) 
    elif type(ast)==Term:
        term_obj = ast
        op = term_obj.op
        x = term_obj.x
        y = term_obj.y
        if op.name == "ADD":
            val1 = get_random_name("int_val")
            val2 = get_random_name("int_val")
            yield (INT,val1,0)
            yield (INT,val2,0)

            for a in compile(x):
                yield a
            yield (LDI,val1,result)

            for a in compile(y):
                yield a
            yield (LDI,val2,result)

            yield (LDI,result,val1)
            yield (ADD,result,val2)
        elif op.name == "SUB":
            val1 = get_random_name("int_val")
            val2 = get_random_name("int_val")
            yield (INT,val1,0)
            yield (INT,val2,0)

            for a in compile(x):
                yield a
            yield (LDI,val1,result)

            for a in compile(y):
                yield a
            yield (LDI,val2,result)

            yield (LDI,result,val1)
            yield (SUB,result,val2)
    elif type(ast)==Block:
        for s in ast.statements:
            for a in compile(s):
                yield a
    elif type(ast)==Var:
        yield (LDI,result,ast.name)            
    elif type(ast)==Logic:
        logic = ast
        val1 = get_random_name("logic_val1")
        val2 = get_random_name("logic_val2")
        c0 = get_random_name("const0")
        c1 = get_random_name("const1")

        yield (INT,val1,0)
        yield (INT,val2,0)
        yield (INT,c0,0)
        yield (INT,c1,1)

        for a in compile(logic.a):
            yield a
        yield (LDI,val1,result)

        for a in compile(logic.b):
            yield a
        yield (LDI,val2,result)

        
        jump_label = get_random_name("logic_jump")
        if logic.op=="==":
            yield (SUB,val2,val1)
            yield (LDI,result,c0)
            yield (JPL,val2,jump_label)
            yield (JMI,val2,jump_label)
            yield (LDI,result,c1)
            yield (jump_label,LDI,result,result)
        elif logic.op==">":
            yield (SUB,val1,val2)
            yield (LDI,result,c1)
            yield (JPL,val1,jump_label)
            yield (LDI,result,c0)
            yield (jump_label,LDI,result,result)
    else:
        raise ast

source = """{
    int i = 0

    int mod_i = 0
    int mod_j = 0
    int rest = 0
    int tmp = 0

    i = 1
label: loop_head
    if (i==20) {
        goto loop_end
    }

    mod_i = i
    mod_j = 15
    goto mod
label: call_back_mod15

    if(rest==0){
        print "FizzBuzz"
        goto loop_tail
    }

    mod_i = i
    mod_j = 3
    goto mod
label: call_back_mod3

    if(rest==0){
        print "Fizz"
        goto loop_tail
    }

    mod_i = i
    mod_j = 5
    goto mod
label: call_back_mod5

    if(rest==0){
        print "Buzz"
        goto loop_tail
    }

    print "{0}" i

label: loop_tail
    i = i + 1
    goto loop_head
label: loop_end
    goto end


label: mod
    rest = mod_i
label: mod_loop_head
    tmp = rest - mod_j
    if(tmp > mod_j) {
        rest = tmp
        goto mod_loop_head
    }
    rest = tmp
    if(tmp==mod_j){
        rest = 0
    }
    if(mod_j==15){
        goto call_back_mod15
    }
    if(mod_j==3){
        goto call_back_mod3
    }
    if(mod_j==5){
        goto call_back_mod5
    }
    


label: end
}"""

import sys

ast = program.parse(source)
print(ast,file=sys.stderr)
seq = [(INT,result,0)]+list(compile(ast))
for a in seq:
    print(a,file=sys.stderr)

from context import Context

c = Context("FsmScript")
walk(c,seq)
print(c.gen())
