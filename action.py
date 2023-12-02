from util import get_random_name

def add_action(state,action):
    actions = get_random_name(f"{action}_actions")
    return """
        var {actions} = new List<FsmStateAction>({state}.Actions);
        {actions}.Add({action});
        {state}.Actions = {actions}.ToArray();

        {state}.SaveActions();
    """.format(**locals())

class FixedWaitAction:
    def __init__(self,time):
        self.time = time

    def dump(self,_state):
        state = _state.var_name
        action = get_random_name(f"fixedWaitAction_{state}")

        return """
        var {action} = new Wait();
        {action}.time = {self.time}f;
        """.format(**locals()) + "\n" + add_action(state,action)

class FormatStringAction:
    def __init__(self,result,format_string,*args):
        self.result = result
        self.format_string = format_string
        self.args = args

    def dump(self,_state):
        def gen():
            state = _state.var_name
            format_string = self.format_string
            args = self.args

            action = get_random_name(f"FormatStringAction_{state}")
            tmp_format_string = f"{action}_vals"

            tmp_variables = get_random_name(f"{action}_vals")

            yield """
        var {action} = new FormatString();
        var {tmp_format_string} = new FsmString("");
        {action}.storeResult = {self.result.var_name};
        {tmp_format_string}.Value = "{format_string}";
        {action}.format = {tmp_format_string};
        var {tmp_variables} = new List<FsmVar>();
        """.format(**locals())

            for v in args:
                
                tmp_var = get_random_name(f"{action}_vals")

                yield """
        var {tmp_var} = new FsmVar({v.var_name});
        {tmp_variables}.Add({tmp_var});
            """.format(**locals())

            yield """
        {action}.variables = {tmp_variables}.ToArray();
            """.format(**locals())

            yield add_action(state,action)
        return "\n".join(gen())

class JumpAction:
    def __init__(self,event):
        self.event = event

    def dump(self,_state):
        def gen():
            state = _state.var_name
            event = self.event.var_name
            action = get_random_name(f"JumpAction_{state}")
            tmp_value = f"{action}_vals"

            yield """
        var {action} = new IntCompare();
        var {tmp_value} = new FsmInt("");
        {tmp_value}.Value = 0;
        {tmp_value}.UseVariable = false;

        {action}.integer1 = {tmp_value};
        {action}.integer2 = {tmp_value};
        {action}.equal = {event};
        """.format(**locals())

            yield add_action(state,action)

        return "\n".join(gen())

class IntAddAction:
    def __init__(self,var,val):
        self.var = var
        self.val = val

    def dump(self,_state):
        state = _state.var_name
        action = get_random_name(f"intAddAction_{state}")

        var = self.var.var_name
        val = self.val.var_name

        return """

        var {action} = new IntAdd();
        {action}.intVariable = {var};
        {action}.add = {val};

        """.format(**locals()) + add_action(state,action)

class DebugLogAction:
    def __init__(self,str_value):
        self.value = str_value

    def dump(self,_state):
        state = _state.var_name
        action = get_random_name(f"setIntCompareAction_{state}")
        tmp_actions = f"{action}_actions"

        return """
        var {action} = new DebugLog();
        {action}.text = {self.value.var_name};
        {action}.sendToUnityLog = true;

        """.format(**locals()) + add_action(state,action)

class SetIntValueAction:
    def __init__(self,int_val,value):
        self.int_val = int_val
        self.value = value

    def dump(self,state):
        state_name = state.var_name
        action_name = get_random_name(f"setIntValueAction_{state_name}")
        tmp_value = f"{action_name}_vals"
        tmp_actions = f"{action_name}_actions"

        return """
        var {action_name} = new SetIntValue();
        var {tmp_value} = new FsmInt("");
        {tmp_value}.Value = {self.value};
        {tmp_value}.UseVariable = false;
        {action_name}.intVariable = {self.int_val.var_name};
        {action_name}.intValue = {tmp_value};

        """.format(**locals()) + add_action(state_name,action_name)

class AssignIntValueAction:
    def __init__(self,int_val,value):
        self.int_val = int_val
        self.value = value

    def dump(self,state):
        state_name = state.var_name
        action_name = get_random_name(f"setIntValueAction_{state_name}")
        tmp_actions = f"{action_name}_actions"

        return """
        var {action_name} = new SetIntValue();
        {action_name}.intVariable = {self.int_val.var_name};
        {action_name}.intValue = {self.value.var_name};

        """.format(**locals()) + add_action(state_name,action_name)

class IntOperatorAction:
    def __init__(self,i1,op,i2,result):
        self.i1 = i1
        self.op = op
        self.i2 = i2
        self.result = result

    def dump(self,_state):
        state = _state.var_name
        action = get_random_name(f"intOperator_{state}")

        return """
        var {action} = new IntOperator();
        {action}.integer1 = {self.i1.var_name};
        {action}.integer2 = {self.i2.var_name};
        {action}.operation = IntOperator.Operation.{self.op};
        {action}.storeResult = {self.result.var_name};
        """.format(**locals()) + add_action(state,action)

class IntCompareAction:
    def __init__(self,int_val1,int_val2,equal_event=None,less_than_event=None,greater_than_event=None):
        self.int_val1 = int_val1
        self.int_val2 = int_val2
        self.equal_event = equal_event
        self.less_than_event = less_than_event
        self.greater_than_event = greater_than_event

    def dump(self,_state):
        def gen():
            state = _state.var_name
            action = get_random_name(f"setIntCompareAction_{state}")
            tmp_actions = f"{action}_actions"

            i1 = self.int_val1.var_name
            i2 = self.int_val2.var_name

            yield """
        var {action} = new IntCompare();
        {action}.integer1 = {i1};
        {action}.integer2 = {i2};
        """.format(**locals())

            if self.equal_event:
                yield f"        {action}.equal = {self.equal_event.var_name};"
            if self.less_than_event:
                yield f"        {action}.lessThan = {self.less_than_event.var_name};"
            if self.greater_than_event:
                yield f"        {action}.greaterThan = {self.greater_than_event.var_name};"

            yield add_action(state,action)

        return "\n".join(gen())