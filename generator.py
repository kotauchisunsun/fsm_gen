from state import StateContext

class Generator:
    def __init__(self,name):
        self.name = name
        self.int_vals = []
        self.str_vals = []
        self.bool_vals = []
        self.states = []
        self.events = []
        self.transitions = []
        self.start_state = None

    def add_state(self,state):
        self.states.append(state)

    def set_start_state(self,state):
        if state not in self.states:
            raise f"{from_state} state not Found"
        self.start_state = state

    def add_event(self,event):
        self.events.append(event)

    def add_transition(self,transition):
        
        if transition.from_state not in self.states:
            raise f"{from_state} state not Found"
        if transition.to_state not in self.states:
            raise f"{to_state} state not Found"
        if transition.event not in self.events and transition.event.name != "FINISHED":
            raise f"{event.name} event not Found"

        self.transitions.append(transition)

    def gen_transition(self):
        return "\n".join(t.dump() for t in self.transitions)
    
    def add_int(self,val):
        self.int_vals.append(val)

    def add_str(self,val):
        self.str_vals.append(val)

    def add_bool(self,val):
        self.bool_vals.append(val)

    def gen_int(self):
        return "\n".join(i.dump("variables") for i in self.int_vals)

    def gen_bool(self):
        return "\n".join(i.dump("variables") for i in self.bool_vals)
        
    def gen_str(self):
        return "\n".join(i.dump("variables") for i in self.str_vals)


    def make_level(self):
        queue = [self.start_state]
        level = dict()
        count = 0

        while len(queue) > 0:
            next_queue = []
            local_count = 0
            while len(queue) > 0:
                s = queue.pop()

                key = s.name
                if key in level:
                    continue

                level[key] = (count,local_count)

                for ns in (t.to_state for t in self.transitions if t.from_state is s):
                    next_queue.append(ns)

                local_count += 1
            count += 1
            queue = next_queue

        return level
        
    def gen_state(self):
        level = self.make_level()
        def _():
            for s in self.states:
                yi,xi = level[s.name]
                context = StateContext("stateList",300+300*xi,100+80*yi)
                yield s.dump(context)
        return "\n".join(_())

    def gen_event(self):
        return "\n".join(s.dump("events") for s in self.events)

    def gen_startup(self):
        return (
"""
        var start_transition = new FsmTransition();
        start_transition.FsmEvent = event_FINISHED;
        start_transition.ToState = {var_name}.Name;
        start_transition.ToFsmState = {var_name};

        var transitions = new List<FsmTransition>(firstState.Transitions);
        transitions.Add(start_transition);
        firstState.Transitions = transitions.ToArray();
""".format(var_name=self.start_state.var_name)
)

    def gen(self):
        state_src = self.gen_state()
        events_src = self.gen_event()
        transitions_src = self.gen_transition()
        startup_src = self.gen_startup()
        int_src = self.gen_int()
        bool_src = self.gen_bool()
        str_src = self.gen_str()

        variable_src = int_src + "\n" + bool_src + "\n" + str_src
        return (
"""
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEditor;
using HutongGames.PlayMaker;
using HutongGames.PlayMaker.Actions;

public class %s
{
    [MenuItem("EditorFSM/%s")]
    private static void Gen(){
        var go = GameObject.Find("%s");
        var fsmEditor = go.AddComponent<PlayMakerFSM>();

        var fsm = fsmEditor.Fsm;
        fsm.MaxLoopCountOverride = 100000000;
        var variables = fsm.Variables;

        %s
    
        var event_FINISHED = FsmEvent.FindEvent("FINISHED");

        var events = new List<FsmEvent>(fsm.Events);
        events.Add(event_FINISHED);
        %s
        fsm.Events = events.ToArray();

        var states = fsm.States;
        var firstState = fsm.States[0];

        var stateList = new List<FsmState>(states);
        %s
        fsm.States = stateList.ToArray();

        %s
        %s
    }
}
"""%(self.name,self.name,self.name,variable_src,events_src,state_src,transitions_src,startup_src)
    )
