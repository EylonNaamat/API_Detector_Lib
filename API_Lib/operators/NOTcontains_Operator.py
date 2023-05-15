
"""
this class represent a operator (!@contains) and this class contain the function that should run when this
operator appears in rule.operator
for checking the rule with this operator you should creat instance of this class and run his function validate()
with the needed parameters
this operator check if the word/text is not in one of the field in the places list(the places that the rule ask to look
for)
"""
class NOTcontains_Operator:
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
                match = expression in sys_request.get(out_place).get(in_place)
                match = not match
                if match:
                    return True
        return False

    """
    helper function to validate
    this function work on place that contain dict object
    this function check if the rule is being triggered by the place
    """
    def check_dict_place(self, sys_request, place, expression):
        for val in sys_request.get(place).values():
            match = expression in val
            match = not match
            if match:
                return True
        return False

    """
    helper function to validate
    this function work on place that contain list object
    this function check if the rule is being triggered by the place
    """
    def check_list_place(self, sys_request, place, expression):
        for key in sys_request.get(place):
            match = expression in key
            match = not match
            if match:
                return True
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
                    return True
            else:
                if sys_request.get(place) is not None:
                    if isinstance(sys_request.get(place), dict):
                        detected = self.check_dict_place(sys_request, place, expression)
                        if detected:
                            return True
                    else:
                        if isinstance(sys_request.get(place), list):
                            detected = self.check_list_place(sys_request, place, expression)
                            if detected:
                                return True
                        else:
                            match = expression in sys_request.get(place)
                            match = not match
                            if match:
                                return True
        return False
