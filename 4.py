from context import Context
from action import *
from macro import Macro
from op import *

c = Context("FsmHoge")

s1,s2 = c.add_states("s1","s2")
c.set_start_state(s1)

i1 = c.add_int("i1",15)
ci7 = c.add_const_int(7)
rest = c.add_int("rest")

mod_macro= mod_op(c,i1,ci7,rest)

c.add_transition(s1,c.finished_event,mod_macro.start)
c.add_transition(mod_macro.end,c.finished_event,s2)

print(c.gen())