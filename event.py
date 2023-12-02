class Event:
    def __init__(self,name):
        self.__name = name

    @property
    def name(self):
        return self.__name

    @property
    def var_name(self):
        return "event_%s"%(self.__name)

    def __str__(self):
        return f"Event(name={self.name},var_name={self.var_name})"

    def dump(self,event_list):
        return """
        var {var_name} = new FsmEvent("{name}");
        {event_list}.Add({var_name});
""".format(var_name=self.var_name,name=self.name,event_list=event_list)