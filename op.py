from macro import Macro
from action import *

class ForOpContext:
    def __init__(self,c,init_val,end_val,step_val,counter):
        self.c = c
        self.inner_block = block_op(c,"inner_for")
        block = for_op(c,init_val,end_val,step_val,counter,self.inner_block)
        self.start = block.start
        self.end = block.end

    def __enter__(self):
        return self.inner_block

    def __exit__(self, exception_type, exception_value, traceback):
        pass

class IntEqualOpContext:
    def __init__(self,c,var,val):
        self.inner_block = block_op(c,"inner_int_equal_op")
        block = int_compare_op(c,var,val,self.inner_block)
        self.start = block.start
        self.end = block.end

    def __enter__(self):
        return self.inner_block

    def __exit__(self, exception_type, exception_value, traceback):
        pass
    
def block_op(c,prefix=""):
    pprefix = "" if prefix == "" else prefix + "_"
    start = c.add_tmp_state(pprefix + "block_start")
    end = c.add_tmp_state(pprefix + "block_end")

    return Macro(start,end)

def jump(c,from_state,to_state):
    e1 = c.add_tmp_event()

    from_state.add_action(
        JumpAction(e1)
    )

    c.add_transition(from_state,e1,to_state)    

def for_op(c,init_val,end_val,step_val,counter,block):
    for_block = block_op(c,"for")
    start = for_block.start
    end = for_block.end

    break_event = c.add_tmp_event()

    start.add_action(
        AssignIntValueAction(counter,init_val)
    )

    loop_head = c.add_tmp_state("loop_head")
    loop_head.add_action(
        IntCompareAction(counter,end_val,break_event,None,break_event)
    )

    loop_tail = c.add_tmp_state("loop_tail")
    loop_tail.add_actions(
        IntOperatorAction(counter,"Add",step_val,counter)
    )

    c.add_transition(loop_tail,c.finished_event,loop_head)
    c.add_transition(loop_head,break_event,end)
    c.add_sequence_transitions(
        start,
        loop_head,
        block.start
    )

    c.next(
        block.end,
        loop_tail
    )
    
    return for_block

def int_compare_op(c,var,val,equal_block):
    int_compare_op_block = block_op(c,"int_compare_op")
    start = int_compare_op_block.start
    end = int_compare_op_block.end

    equal_event = c.add_tmp_event()

    start.add_action(
        IntCompareAction(var,val,equal_event)
    )

    c.add_transition(start,equal_event,equal_block.start)
    c.next(equal_block.end,end)

    c.next(start,end)

    return Macro(start,end)

def mod_op(c,i1,i2,rest):
    block = block_op(c,"mod")
    tmp = c.add_tmp_int()
    start = block.start
    loop = c.add_tmp_state("mod_loop")
    end = block.end

    e1 = c.add_tmp_event()

    start.add_actions(
        AssignIntValueAction(tmp,i1),
    )

    loop.add_actions(
        IntCompareAction(tmp,i2,None,e1,None),
        IntOperatorAction(tmp,"Subtract",i2,tmp)
    )

    end.add_actions(
        AssignIntValueAction(rest,tmp)
    )

    c.add_sequence_transitions(
        start,
        loop
    )

    c.add_transition(loop,c.finished_event,loop)
    c.add_transition(loop,e1,end)

    return block