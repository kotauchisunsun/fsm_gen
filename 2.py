from context import Context
from action import *

c = Context("FsmHoge")
s1 = c.add_state("s1")
s21 = c.add_state("s21")
s22 = c.add_state("s22")
s23 = c.add_state("s23")

c.set_start_state(s1)

i1 = c.add_int("i1")
i2 = c.add_int("i2")

sv1 = c.add_str("sv1")

e1 = c.add_event("e1")
e2 = c.add_event("e2")
e3 = c.add_event("e3")

s1.add_action(
    SetIntValueAction(i1,10)
)

s1.add_action(
    IntCompareAction(i1,i2,e1,e2,e3)
)

c.add_transition(s1,e1,s21)
c.add_transition(s1,e2,s22)
c.add_transition(s1,e3,s23)

print(c.gen())