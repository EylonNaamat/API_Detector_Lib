"""
this class represent the system rule object that we build from reading the conf files
"""
class SYS_Rule:

    def __init__(self, place_to_lookfor, operator, args, extra_info):
        self.id = extra_info['id']
        self.msg = extra_info['msg']
        self.tags = extra_info['tags']
        self.severity = extra_info['severity']
        self.place_to_lookfor = [place.lower() for place in place_to_lookfor]
        self.action = extra_info['action']
        self.operator = operator
        self.args = args
        self.child_rule = None

    # if the rule depend on other rule we add it as child rule
    def add_child_rule(self, new_child_rule):
        if self.child_rule is None:
            self.child_rule = new_child_rule
        else:
            self.child_rule.add_child_rule(new_child_rule)

    def __repr__(self):
        return f"id :{self.id}\n msg:{self.msg }\n tags:{self.tags}\n severity {self.severity}\n place_to_lookfor:{self.place_to_lookfor}\n operator:{self.operator}\n args:{self.args}\n child:{self.child_rule}"
    def __str__(self):
        return f"id :{self.id}\n msg:{self.msg }\n tags:{self.tags}\n severity {self.severity}\n place_to_lookfor:{self.place_to_lookfor}\n operator:{self.operator}\n args:{self.args}\n child:{self.child_rule}"