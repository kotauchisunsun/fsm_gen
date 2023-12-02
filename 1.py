from state import State, StateContext
from event import Event
from transition import Transition
from int_val import IntVal
from bool_val import BoolVal
from generator import Generator
from action import *

generator = Generator("FsmHoge")
finished_event = Event("FINISHED")

i1 = IntVal("i1")
generator.add_int(i1)

i2 = IntVal("i2")
generator.add_int(i2)

b1 = BoolVal("b1")
generator.add_bool(b1)

event1 = Event("event1")
event2 = Event("event2")
event3 = Event("event3")
generator.add_event(event1)
generator.add_event(event2)
generator.add_event(event3)

state1 = State("state1")
state1.add_action(
    SetIntValueAction(i1,10)
)
generator.add_state(state1)

state2 = State("state2")
state2.add_action(
    AssignIntValueAction(i2,i1)
)
generator.add_state(state2)

transition1 = Transition(state1,finished_event,state2)
generator.add_transition(transition1)

generator.set_start_state(state1)
print(generator.gen())
