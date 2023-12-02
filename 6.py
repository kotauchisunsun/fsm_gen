from context import Context
from action import *
from op import *
from state import State

c = Context("FsmHoge")
State.DEBUG = True
State.ACTION_WAIT_TIME = 0.01
State.STATE_WAIT_TIME = 0.01

entire = block_op(c,"entire")
s1,s2 = entire.start,entire.end
c.set_start_state(s1)

i = c.add_int("i")
init = c.add_const_int(1)
end = c.add_const_int(20)
step = c.add_const_int(1)

for_op_context = ForOpContext(c,init,end,step,i)
c.next(s1,for_op_context.start)

with for_op_context as repeat_block:
    c15 = c.add_const_int(15)
    c0 = c.add_const_int(0)
    rest = c.add_int("rest")

    mod15_block = mod_op(c,i,c15,rest)
    c.next(repeat_block.start,mod15_block.start)

    mod15_int_equal_op_context = IntEqualOpContext(c,rest,c0)

    c.add_sequence_block(
        mod15_block,
        mod15_int_equal_op_context
    )

    with mod15_int_equal_op_context as mod15_equal0_block:
        s15 = c.add_const_str("FizzBuzz")

        mod15_equal0_block.start.add_action(
            DebugLogAction(s15)
        )

        jump(c,mod15_equal0_block.start,repeat_block.end)

        c.short(mod15_equal0_block)


    c5 = c.add_const_int(5)
    mod5_block = mod_op(c,i,c5,rest)
    mod5_int_equal_op_context = IntEqualOpContext(c,rest,c0)
    
    c.add_sequence_block(
        mod15_int_equal_op_context,
        mod5_block,
        mod5_int_equal_op_context
    )

    with mod5_int_equal_op_context as mod5_equal0_block:
        s5 = c.add_const_str("Buzz")

        mod5_equal0_block.start.add_action(
            DebugLogAction(s5)
        )

        jump(c,mod5_equal0_block.start,repeat_block.end)

        c.short(mod5_equal0_block)



    c3 = c.add_const_int(3)
    mod3_block = mod_op(c,i,c3,rest)
    mod3_int_equal_op_context = IntEqualOpContext(c,rest,c0)

    c.add_sequence_block(
        mod5_int_equal_op_context,
        mod3_block,
        mod3_int_equal_op_context
    )

    with mod3_int_equal_op_context as mod3_equal0_block:
        s3 = c.add_const_str("Fizz")

        mod3_equal0_block.start.add_action(
            DebugLogAction(s3)
        )

        jump(c,mod3_equal0_block.start,repeat_block.end)

        c.short(mod3_equal0_block)

    num_out_state = c.add_tmp_state()
    output = c.add_str("output")
    num_out_state.add_actions(
        FormatStringAction(
            output,
            "{0}",
            i
        ),
        DebugLogAction(
            output
        )
    )

    c.next(mod3_int_equal_op_context.end,num_out_state)
    c.next(num_out_state,repeat_block.end)

c.next(for_op_context.end,s2)


print(c.gen())