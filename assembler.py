from context import Context
from state import State

from asm import * 

def is_op(text):
    return any(
        text == o.name
        for o
        in ops
    )

def get_op(text):
    for o in ops:
        if text == o.name:
            return o
    raise "Error"

def assemble(name,source,action_wait_time,state_wait_time):
    c = Context(name)
    State.DEBUG = True
    State.ACTION_WAIT_TIME = action_wait_time
    State.STATE_WAIT_TIME = state_wait_time

    def parse():
        for line in source.split("\n"):

            if(";" in line):
                line = line[:line.index(";")]

            line = line.strip()

            if len(line)==0:
                continue

            args = line.split()

            label = None
            if not is_op(args[0]):
                label = args[0]
                del args[0]

            asm_op = get_op(args[0])
            if asm_op == INT:
                args[2] = int(args[2])
            
            if label:
                yield (label,asm_op,*args[1:])
            else:
                yield (asm_op,*args[1:])

    walk(c,list(parse()))
    return c.gen()

if True:            
    seq = assemble("Temp",
    """
    INT i 10
    INT j 10
    STR k "hoge"
    FMS k "{0},{1}" i j
    PRT k
    """,
        0.01,
        0.01
    )

    print (seq)