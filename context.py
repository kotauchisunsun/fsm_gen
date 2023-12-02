from state import State, StateContext
from event import Event
from transition import Transition
from int_val import IntVal,StrVal
from bool_val import BoolVal
from generator import Generator
from action import *
from util import get_random_name

class Context:
    def __init__(self,name):
        self.generator = Generator(name)
        self.finished_event = Event("FINISHED")
        self.vars = dict()
        self.states = dict()

    def get_var(self,name):
        return self.vars[name]

    def get_state(self,name):
        return self.states[name]

    def exists_state(self,name):
        return name in self.states

    def add_int(self,name,value=None):
        i1 = IntVal(name,value)
        self.generator.add_int(i1)
        self.vars[name] = i1
        return i1

    def add_tmp_int(self):
        name = get_random_name("tmp_int_")
        return self.add_int(name)

    def add_const_int(self,value):
        name = get_random_name("const_int_")
        i1 = IntVal(name,value)
        self.generator.add_int(i1)
        return i1       

    def add_bool(self,name):
        b1 = BoolVal(name)
        self.generator.add_bool(b1)
        self.vars[name] = b1
        return b1

    def add_str(self,name,value=None):
        s1 = StrVal(name,value)
        self.generator.add_str(s1)
        self.vars[name] = s1
        return s1
    
    def add_const_str(self,value):
        name = get_random_name("const_str_")
        return self.add_str(name,value)

    def add_event(self,name):
        e1 = Event(name)
        self.generator.add_event(e1)
        return e1

    def add_tmp_event(self):
        name = get_random_name("tmp_event_")
        return self.add_event(name)

    def add_state(self,name):
        state1 = State(name)
        self.generator.add_state(state1)
        self.states[name] = state1
        return state1

    def add_states(self,*args):
        return tuple(
            self.add_state(name)
            for name
            in args
        )

    def add_tmp_state(self,prefix="tmp_state"):
        name = get_random_name(prefix)
        return self.add_state(name)

    def add_transition(self,s1,e1,s2):
        t = Transition(s1,e1,s2)
        self.generator.add_transition(t)
        return t

    def next(self,s1,s2):
        return self.add_transition(s1,self.finished_event,s2)

    def short(self,block):
        return self.next(block.start,block.end)

    def add_sequence_transitions(self,*args):
        for s1,s2 in zip(args[:-1],args[1:]):
            self.add_transition(s1,self.finished_event,s2)

    def add_sequence_block(self,*args):
        for b1,b2 in zip(args[:-1],args[1:]):
            self.next(b1.end,b2.start)

    def set_start_state(self,state):
        self.generator.set_start_state(state)

    def gen(self):
        return self.generator.gen()