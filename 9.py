from context import Context
from op import *
from state import State

from asm import * 

c = Context("FsmFizzBuzz")
State.DEBUG = True
State.ACTION_WAIT_TIME = 0.00
State.STATE_WAIT_TIME = 0.01

seq = (
    (
        (INT,"i",0),
        (INT,"init",1),
        (INT,"end",20),
        (INT,"step",1),
        (INT,"result",0),
        (INT,"c3",3),
        (INT,"c5",5),
        (INT,"c15",15),

        (INT,"tmp",0),
        (INT,"rest",0),
        (STR,"out",""),

        (STR,"s15","FizzBuzz"),
        (STR,"s3","Fizz"),
        (STR,"s5","Buzz"),

        #head
        (LDI,"i","init"),
        ("loop_head",LDI,"tmp","i"),
        (SUB,"tmp","end"),
        (JPL,"tmp","loop_end"),
        (JZE,"tmp","loop_end")
    ) 
        #Main
    + call_mod("rest","i","c15")
    + ( 
        (JZE,"rest","FizzBuzz"),
        (JMP,"skip15"),
        ("FizzBuzz",PRT,"s15"),
        (JMP,"loop_tail"),
        ("skip15",LDI,"tmp","tmp"),
    )    
    + call_mod("rest","i","c3")
    + ( 
        (JZE,"rest","Fizz"),
        (JMP,"skip3"),
        ("Fizz",PRT,"s3"),
        (JMP,"loop_tail"),
        ("skip3",LDI,"tmp","tmp"),
    )
    + call_mod("rest","i","c5")
    + ( 
        (JZE,"rest","Buzz"),
        (JMP,"skip5"),
        ("Buzz",PRT,"s5"),
        (JMP,"loop_tail"),
        ("skip5",LDI,"tmp","tmp"),
    )
    + (
        (FMS,"out","{0}","i"),
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