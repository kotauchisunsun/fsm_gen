def generate_source(var_name,name,value,variables,tmpVariables,fsm_type,fsm_variables):
    yield """
        var {tmpVariables} = new List<{fsm_type}>({variables}.{fsm_variables});
        var {var_name} = new {fsm_type}("{name}");
    """.format(**locals())

    if value is not None:
        yield """
        {var_name}.Value = {value};
    """.format(**locals())

    yield """
        {tmpVariables}.Add({var_name});
        {variables}.{fsm_variables} = {tmpVariables}.ToArray();
    """.format(**locals())


class IntVal:
    def __init__(self,name,value=None):
        self.name = name
        self.var_name = f"int_{name}"
        self.value = value

    def dump(self,_variables):
        return "\n".join(
            generate_source(
                self.var_name,
                self.name,
                self.value,
                _variables,
                f"tmpIntVariables_{self.var_name}",
                "FsmInt",
                "IntVariables"
            )
        )


class StrVal:
    def __init__(self,name,value):
        self.name = name
        self.var_name = f"str_{name}"
        self.value = value

    def dump(self,variables):
        return "\n".join(
            generate_source(
                self.var_name,
                self.name,
                f'"{self.value}"',
                variables,
                f"tmpStrVariables_{self.var_name}",
                "FsmString",
                "StringVariables"
            )
        )

