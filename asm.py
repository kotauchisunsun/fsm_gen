import types
from util import get_random_name
from action import *

def decl(name):
    t = types.new_class(name)
    t.name = name
    return t

INT = decl("INT") #INT型変数宣言
STR = decl("STR") #STR型変数宣言
ADD = decl("ADD") # A = A + B
SUB = decl("SUB") # A = A - B
JMP = decl("JMP") #無条件ジャンプ
JZE = decl("JZE") #0ジャンプ
JPL = decl("JPL") #正ジャンプ
JMI = decl("JMI") #負ジャンプ
LDI = decl("LDI") #代入 A = B
PRT = decl("PRT") #Debug.log
FMS = decl("FMS") #String.Format

ops = [
    INT,
    STR,
    ADD,
    SUB,
    JMP,
    JZE,
    JPL,
    JMI,
    LDI,
    PRT,
    FMS
]

def gen_state(c,state_name,op):
    if state_name and c.exists_state(state_name):
        return c.get_state(state_name)
    return c.add_tmp_state(op.name)

def walk(c,seq):
    start = c.add_state("start")
    c.set_start_state(start)
    ns = start

    for statement in seq:
        if type(statement[0]) == str:
            c.add_state(statement[0])

    for statement in seq:
        s = list(statement)
        state_name = None
        if type(s[0]) == str:
            state_name = s[0]
            del s[0]

        op = s[0]

        if op==INT:
            c.add_int(s[1],s[2])
        elif op==STR:
            c.add_str(s[1],s[2])
        elif op==ADD:
            tmp = gen_state(c,state_name,op)
            v = c.get_var(s[1])
            a = c.get_var(s[2])
            tmp.add_action(
                IntOperatorAction(v,"Add",a,v)
            )
            c.next(ns,tmp)
            ns = tmp
        elif op==SUB:
            tmp = gen_state(c,state_name,op)
            v = c.get_var(s[1])
            a = c.get_var(s[2])
            tmp.add_action(
                IntOperatorAction(v,"Subtract",a,v)
            )
            c.next(ns,tmp)
            ns = tmp
        elif op==JMP:
            tmp = gen_state(c,state_name,op)
            js = c.get_state(s[1])
            e1 = c.add_tmp_event()
            tmp.add_action(
                JumpAction(e1)
            )
            c.add_transition(tmp,e1,js)
            c.next(ns,tmp)
            ns = tmp      
        elif op==JZE:
            tmp = gen_state(c,state_name,op)
            i1 = c.get_var(s[1])
            c0 = c.add_const_int(0)
            js = c.get_state(s[2])
            e1 = c.add_tmp_event()
            tmp.add_action(
                IntCompareAction(i1,c0,e1)
            )
            c.add_transition(tmp,e1,js)
            c.next(ns,tmp)
            ns = tmp        
        elif op==JPL:
            tmp = gen_state(c,state_name,op)
            i1 = c.get_var(s[1])
            c0 = c.add_const_int(0)
            js = c.get_state(s[2])
            e1 = c.add_tmp_event()
            tmp.add_action(
                IntCompareAction(i1,c0,None,None,e1)
            )
            c.add_transition(tmp,e1,js)
            c.next(ns,tmp)
            ns = tmp    
        elif op==JMI:
            tmp = gen_state(c,state_name,op)
            i1 = c.get_var(s[1])
            c0 = c.add_const_int(0)
            js = c.get_state(s[2])
            e1 = c.add_tmp_event()
            tmp.add_action(
                IntCompareAction(i1,c0,None,e1,None)
            )
            c.add_transition(tmp,e1,js)
            c.next(ns,tmp)
            ns = tmp      
        elif op==LDI:
            tmp = gen_state(c,state_name,op)
            i1 = c.get_var(s[1])
            i2 = c.get_var(s[2])
            tmp.add_action(
                AssignIntValueAction(i1,i2)
            )
            c.next(ns,tmp)
            ns = tmp
        elif op==PRT:
            tmp = gen_state(c,state_name,op)
            s1 = c.get_var(s[1])
            tmp.add_action(
                DebugLogAction(s1)
            )
            c.next(ns,tmp)
            ns = tmp 
        elif op==FMS:
            tmp = gen_state(c,state_name,op)
            r = c.get_var(s[1])
            f = s[2]
            args = [c.get_var(a) for a in s[3:]]
            tmp.add_action(
                FormatStringAction(r,f,*args)
            )
            c.next(ns,tmp)
            ns = tmp 

def call_mod(result,i1,j1):
    i = get_random_name("mod_i")
    j = get_random_name("mod_j")
    rest = get_random_name("mod_rest")
    loop_label = get_random_name("mod_loop_label")

    return (
        (             INT,    i,            0),
        (             INT,    j,            0),
        (             INT, rest,            0),
        (             LDI,    i,           i1),
        (             LDI,    j,           j1),
        (             LDI, rest,            i),
        ( loop_label, LDI, result,       rest),
        (             SUB, rest,            j),
        (             JPL, rest,   loop_label),
        (             JZE, rest,   loop_label)
    )
