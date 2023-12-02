from context import Context
from op import *
from state import State

from asm import * 

c = Context("FsmPrime")
State.DEBUG = True
State.ACTION_WAIT_TIME = 0.00
State.STATE_WAIT_TIME = 1e-8

seq = (
    (
        (INT,"i",0),
        (INT,"j",0),
        (INT,"init",2),
        (INT,"end",100),
        (INT,"step",1),
        (INT,"result",0),
        (INT,"c1",1),

        (INT,"tmp",0),
        (INT,"rest",0),
        (STR,"out",""),

        #head
        (LDI,"i","init"),
        ("loop_head",LDI,"tmp","i"),
        (SUB,"tmp","end"),
        (JPL,"tmp","loop_end"),
        (JZE,"tmp","loop_end"),

        (LDI,"j","i"),
        ("inner_loop",SUB,"j","c1"),

        (LDI,"tmp","j"),
        (SUB,"tmp","c1"),
        (JZE,"tmp","output")
    )
    + call_mod("rest","i","j")
    + (
        (JZE,"rest","loop_tail"),
        (JMP,"inner_loop"),

        #Main
        ("output",FMS,"out","{0}","i"),
        (PRT,"out"),

        #tail
        ("loop_tail",ADD,"i","step"),
        (JMP,"loop_head"),

        #end
        ("loop_end",LDI,"tmp","tmp")
    )
)

walk(c,seq)
print(c.gen())
