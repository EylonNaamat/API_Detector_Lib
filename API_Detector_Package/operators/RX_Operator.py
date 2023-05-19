import re

"""
this class represent a operator (@rx) and this class contain the function that should run when this 
operator appears in rule.operator
for checking the rule with this operator you should creat instance of this class and run his function validate() 
with the needed parameters
this operator check if the regex is in one of the field in the places list(the places that the rule ask to  look for)
"""
class RX_Operator:
    def __init__(self):
        pass
    """
    helper function to validate
    this function work on place with the next pattern : XXXXXX:YYYYYY
    this function check if the rule is being triggered by the place
    """
    def check_inner_place(self, sys_request, out_place, in_place, expression):
        if sys_request.get(out_place) is not None:
            if sys_request.get(out_place).get(in_place) is not None:
                match = re.search(expression, sys_request.get(out_place).get(in_place))
                if match:
                    return (f"{out_place}:{in_place}",sys_request.get(out_place).get(in_place))
        return False

    """
    helper function to validate
    this function work on place that contain dict object
    this function check if the rule is being triggered by the place
    """
    def check_dict_place(self, sys_request, place, expression):
        for val in sys_request.get(place).values():
            match = re.search(expression, val)
            if match:
                return (place,val)
        return False

    """
    helper function to validate
    this function work on place that contain list object
    this function check if the rule is being triggered by the place
    """
    def check_list_place(self, sys_request, place, expression):
        for key in sys_request.get(place):
            match = re.search(expression, key)
            if match:
                return (place,key)
        return False

    """
    this function check if the rule is being triggered by the place
    """
    def validate(self, sys_request, places, expression):
        for place in places:
            place_split = place.split(":")
            if len(place_split) > 1:
                detected = self.check_inner_place(sys_request, place_split[0], place_split[1], expression)
                if detected:
                    return detected
            else:
                if sys_request.get(place) is not None:
                    if isinstance(sys_request.get(place), dict):
                        detected = self.check_dict_place(sys_request, place, expression)
                        if detected:
                            return detected
                    else:
                        if isinstance(sys_request.get(place), list):
                            detected = self.check_list_place(sys_request, place, expression)
                            if detected:
                                return detected
                        else:
                            print("----------------------------------------------------")
                            print(place)
                            print(sys_request.get(place))
                            print(type(sys_request.get(place)))
                            print("----------------------------------------------------")
                            match = re.search(expression, sys_request.get(place))
                            if match:
                                return (place,sys_request.get(place))
        return False
