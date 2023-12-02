
from context import Context
from action import *
from op import *

c = Context("FsmHoge")

s1,s2 = c.add_states("s1","s2")
c.set_start_state(s1)

block = block_op(c)
c.next(block.start,block.end)

i = c.add_int("i")
init = c.add_const_int(0)
end = c.add_const_int(10)
step = c.add_const_int(1)

for_block = for_op(c,init,end,step,i,block)

c.next(s1,for_block.start)
c.next(for_block.end,s2)

print(c.gen())