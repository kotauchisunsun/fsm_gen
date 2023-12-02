from op import *

class State:
    DEBUG = False
    ACTION_WAIT_TIME = 0.1
    STATE_WAIT_TIME = 1.0

    def __init__(self,name):
        self.__name = name
        self.actions = []

    @property
    def name(self):
        return self.__name

    @property
    def var_name(self):
        return "state_%s"%(self.__name)

    def add_action(self,action):
        if State.DEBUG:
            self.actions.append(
                FixedWaitAction(State.ACTION_WAIT_TIME)
            )
        self.actions.append(action)

    def add_actions(self,*actions):
        for action in actions:
            self.add_action(action)

    def dump(self,context):
        if State.DEBUG:
            self.actions.append(
                FixedWaitAction(State.STATE_WAIT_TIME)
            )

        var_name = self.var_name
        rect = f"rect_{self.var_name}"

        declare_state = """
        var {var_name} = new FsmState(fsm);
        {var_name}.Name = "{self.name}";
        var {rect} = {var_name}.Position;
        {rect}.x = {context.x};
        {rect}.y = {context.y};
        {var_name}.Position = {rect};
        {context.state_list}.Add({var_name});
""".format(**locals())

        declare_action = "\n".join(a.dump(self) for a in self.actions)

        return declare_state + "\n" + declare_action

class StateContext:
    def __init__(self,state_list,x,y):
        self.state_list = state_list
        self.x = x
        self.y = y

    def next(self):
        return StateContext(self.state_list,self.x,self.y+50)
