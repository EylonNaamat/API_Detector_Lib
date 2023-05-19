from .operators.RX_Operator import RX_Operator
from .operators.pmFromFile_Operator import pmFromFile_Operator
from .operators.NOTpmFromFile_Operator import NOTpmFromFile_Operator
from .operators.NOTRX_Operator import NOTRX_Operator
from .operators.contains_Operator import contains_Operator
from .operators.NOTcontains_Operator import NOTcontains_Operator
from .operators.ipMatch_Operator import ipMatch_Operator
from .operators.PM_Operator import PM_Operator
from .operators.NOTPM_Operator import NOTPM_Operator
from .operators.EQ_Operator import EQ_Operator
from .operators.NOTEQ_Operator import NOTEQ_Operator
from .operators.endsWith_Operator import endsWith_Operator

"""
this class is the class that represent the functional part of the system
this class creat all the operator instances and save it in dict
by using the function exec this class get the request and the rule you want to check and check if the rule
is being triggered by the request
"""
class SYS_Operators:
    def __init__(self):
        self.operators = {}
        self.operators['@rx'] = RX_Operator()
        self.operators['!@rx'] = NOTRX_Operator()
        self.operators['@pmFromFile'] = pmFromFile_Operator()
        self.operators['!@pmFromFile'] = NOTpmFromFile_Operator()
        self.operators['!@contains'] = NOTcontains_Operator()
        self.operators['@contains'] = contains_Operator()
        self.operators['@ipMatch'] = ipMatch_Operator()
        self.operators['@pm'] = PM_Operator()
        self.operators['!@pm'] = NOTPM_Operator()
        self.operators['@eq'] = EQ_Operator()
        self.operators['!@eq'] = NOTEQ_Operator()
        self.operators['@endsWith'] = endsWith_Operator()



    def exec(self, rule, request):
        # if the rule action is pass we ignore it
        if rule.action == "pass":
            return False
        # we run on all the place lis in the rule
        # and when we see a place which start with '!' we remove this place from the request and the list
        remain_Places = []
        for place in rule.place_to_lookfor:
            if place[0] == "!":
                temp_place = place.split(":")
                # if the request doesn't have that field we will not need to remove it.
                try:
                    del request.get(temp_place[0][1:])[temp_place[1]]
                except:
                    pass
            else:
                remain_Places.append(place)
        # change the old place list for the new one
        rule.place_to_lookfor = remain_Places

        # here we check rule with child and if so we will check all the rule and their children
        # if one of them will be false we will return false
        # only if all triggered we will return true
        while rule.child_rule is not None:
            if not self.operators[rule.operator].validate(request, rule.place_to_lookfor , rule.args):
                return False
            rule = rule.child_rule
        check_ans = self.operators[rule.operator].validate(request, rule.place_to_lookfor , rule.args)
        return check_ans
