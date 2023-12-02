from context import Context
from op import *
from state import State

from asm import * 

c = Context("FsmHoge")
State.DEBUG = True
State.ACTION_WAIT_TIME = 0.01
State.STATE_WAIT_TIME = 0.01

"""
seq = (
    (INT,"i",10),
    (INT,"c1",1),
    (INT,"i20",20),
    (STR,"s","hogehoge"),
    (LDI,"i","i20"),
    ("sub_state",SUB,"i","c1"),
    (JZE,"i","add_state"),
    (JMP,"sub_state"),
    ("add_state",ADD,"i","c1")
)
"""

"""
seq = (
    (INT,"i",10),
    (INT,"j",3),
    (INT,"rest",0),
    (INT,"mod",0),
    (LDI,"rest","i"),
    ("loop",LDI,"mod","rest"),
    (SUB,"rest","j"),
    (JPL,"rest","loop"),
    (JZE,"rest","loop")
)
"""

"""
seq = (
    (
        (INT,"i",10),
        (INT,"j",3),
        (INT,"c11",11),
        (INT,"c03",3),
        (INT,"c02",2),
        (INT,"rest11",0),
        (INT,"rest03",0),
        (INT,"rest02",0),
    ) 
    + (
        (LDI,"j","c11"),
    )
    + call_mod("rest11","i","j")
    + (
        (LDI,"j","c03"),
    )
    + call_mod("rest03","i","j")
    + (
        (LDI,"j","c02"),
    )
    + call_mod("rest02","i","j")
)
"""


"""
seq = (
    (STR,"a","A"),
    (STR,"b","B"),
    (STR,"c","C"),
    (STR,"result","result"),
    (FMS,"result","Hello"),
    (PRT,"result"),
    (FMS,"result","{0}","a"),
    (PRT,"result"),
    (FMS,"result","{0} {1}","a","b"),
    (PRT,"result"),
)
"""

print(c.gen())