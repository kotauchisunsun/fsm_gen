from context import Context
from asm import * 
c = Context("FsmAsmLoop")

seq = (
    (INT,"i",0),
    (INT,"end",10),
    (INT,"step",1),

    (INT,"tmp",0),
    (STR,"out",""),

    #head
    ("loop_head",LDI,"tmp","i"),
    (SUB,"tmp","end"),
    (JPL,"tmp","loop_end"),
    (JZE,"tmp","loop_end"),

    #Main
    (FMS,"out","{0}","i"),
    (PRT,"out"),

    #tail
    ("loop_tail",ADD,"i","step"),
    (JMP,"loop_head"),

    #end
    ("loop_end",LDI,"tmp","tmp")
)

walk(c,seq)
print(c.gen())