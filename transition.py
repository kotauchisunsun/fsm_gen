from util import get_random_name

class Transition:
    def __init__(self,from_state,event,to_state):
        self.from_state = from_state
        self.event = event
        self.to_state = to_state

    def dump(self):
        from_var = self.from_state
        event_var = self.event
        to_var = self.to_state

        trans_name = get_random_name("transtion_%s_%s_%s"%(from_var.var_name,event_var.var_name,to_var.var_name))
        var_transitions = get_random_name("transitions_%s"%(from_var.var_name))

        return """
        var {trans_name} = new FsmTransition();
        {trans_name}.FsmEvent = {event_var.var_name};
        {trans_name}.ToState = {to_var.var_name}.Name;
        {trans_name}.ToFsmState = {to_var.var_name};

        var {var_transitions} = new List<FsmTransition>({from_var.var_name}.Transitions);
        {var_transitions}.Add({trans_name});
        {from_var.var_name}.Transitions = {var_transitions}.ToArray();
""".format(**locals())