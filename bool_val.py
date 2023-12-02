
class BoolVal:
    def __init__(self,name):
        self.name = name
        self.var_name = f"int_{name}"

    def dump(self,variables):
        tmpBoolVariables = f"tmpBoolVariables_{self.var_name}"
        return (
"""
        var {tmpBoolVariables} = new List<FsmBool>({variables}.BoolVariables);
        var {self.var_name} = new FsmBool("{self.name}");
        {tmpBoolVariables}.Add({self.var_name});
        {variables}.BoolVariables = {tmpBoolVariables}.ToArray();
""".format(**locals()))