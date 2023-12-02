from context import Context
from action import *

c = Context("FsmHoge")

s1,s2 = c.add_states("s1","s2")
c.set_start_state(s1)

i1 = c.add_int("i1",0)
ci1 = c.add_const_int(1)
ci10 = c.add_const_int(10)

e1 = c.add_event("e1")

s1.add_actions(
    IntCompareAction(i1,ci10,e1,None,None),
    IntAddAction(i1,ci1)
)

c.add_transition(s1,c.finished_event,s1)
c.add_transition(s1,e1,s2)

print(c.gen())