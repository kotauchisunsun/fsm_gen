from context import Context
from action import *
from op import *

c = Context("FsmHoge")

entire = block_op(c,"entire")
s1,s2 = entire.start,entire.end
c.set_start_state(s1)

c1 = c.add_const_int(1)
c2 = c.add_const_int(3)
c3 = c.add_const_int(5)

sv1 = c.add_str("result")

s2.add_actions(
    FormatStringAction(
        sv1,
        "{0} {1} {2}",
        c1,
        c2,
        c3
    ),
    DebugLogAction(
        sv1
    )
)

jump(c,s1,s2)

print(c.gen())