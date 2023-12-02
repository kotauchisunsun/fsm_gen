from parsy import regex,string,decimal_digit,seq,whitespace,generate,success
var = regex("[a-zA-Z_]+[a-zA-Z0-9]*")
digit = regex(r'[-+]?[1-9]*[0-9]')

factor_op = string("*") | string("/")
term_op = string("+") | string("-")

atom = digit | var

lp = string("(")
rp = string(")")


lbrace = string("{")
rbrace = string("}")

blank_line = regex("[\s\n]*")
w = whitespace
_ = regex("[_\s]*")


@generate
def statement():
    return (yield if_block | var | digit)

@generate
def line():
    return (yield _ >> statement << _ << regex("\n*"))

@generate
def block():
    value = line
    return (yield lbrace >> blank_line >> value.many() << blank_line << rbrace)

@generate
def if_block():
    return (yield seq(string("if")>>_>>lp>>_>>rp>>_>>block))

parser = block

source = """{
    a
    1
    if(){
        a
    }
}"""

print(parser.parse(source))