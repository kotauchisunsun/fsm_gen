from parsy import regex,string,decimal_digit,seq,whitespace,generate,success

var = regex("[a-zA-Z_]+[a-zA-Z0-9]*")
digit = regex(r'[-+]?[1-9]*[0-9]')

factor_op = string("*") | string("/")
term_op = string("+") | string("-")

atom = digit | var

lp = string("(")
rp = string(")")

@generate
def multiplicative():
    res = yield simple
    res = [res]
    while True:
        operation = yield factor_op | success("")
        if not operation:
            break
        operand = yield simple
        res = [operation,res,operand]
    print("back multi")
    print(res)
    return res

@generate
def additive():
    res = yield multiplicative
    res = [res]
    while True:
        operation = yield term_op | success("")
        if not operation:
            break
        operand = yield multiplicative
        res = [operation,res,operand]
    print("back add")
    print(res)
    return res

expr = additive
simple = (lp >> expr << rp) | atom

def debug(p):
    def _(atom,indent):
        if type(atom) != list:
            print(" "*indent,atom,",")
            return
        print(" "*indent,"[")
        for a in atom:
            _(a,indent+4)
        print(" "*indent,"]")
    _(p,0)

debug(expr.parse("a*(2+1)+1"))
print("piyo")