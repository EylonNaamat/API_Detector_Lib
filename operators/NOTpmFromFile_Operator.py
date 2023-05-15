import os

"""
this class represent a operator (!@pmFromFile) and this class contain the function that should run when this 
operator appears in rule.operator
for checking the rule with this operator you should creat instance of this class and run his function validate() 
with the needed parameters
this class also need the .data file
this operator check if the words in the data files is not in one of the field in the places list(the places that the rule 
ask to look for)

"""
class NOTpmFromFile_Operator:
    def __init__(self, data_files_folder):
        self.data_files_folder = data_files_folder
        self.data_files = {}
        self.load_data_files()
    """
    load all the .data file from the rule folder in to a dict when the file name is the key and the value is a list 
    of all the lines in the file
    """
    def load_data_files(self):
        rule_files = [f for f in os.listdir(self.data_files_folder) if f.endswith('.data')]
        for rulefile in rule_files:
            # read the content
            rule_file_path = os.path.join(self.data_files_folder, rulefile)
            with open(rule_file_path, 'r') as f:
                self.data_files[rulefile] = [line.strip() for line in f.readlines() if line.strip() != '' and line.strip()[0] != '#']

    """
    helper function to validate
    this function work on place with the next pattern : XXXXXX:YYYYYY
    this function check if the rule is being triggered by the place
    """
    def check_inner_place(self, sys_request, out_place, in_place, expression):
        if sys_request.get(out_place) is not None:
            if sys_request.get(out_place).get(in_place) is not None:
                for pattern in self.data_files[expression]:
                    match = pattern in sys_request.get(out_place).get(in_place)
                    if match:
                        return False
        return True
    """
    helper function to validate
    this function work on place that contain dict object
    this function check if the rule is being triggered by the place
    """
    def check_dict_place(self, sys_request, place, expression):
        for val in sys_request.get(place).values():
            for pattern in self.data_files[expression]:
                match = pattern in val
                if match:
                    return False
        return True
    """
    helper function to validate
    this function work on place that contain list object
    this function check if the rule is being triggered by the place
    """
    def check_list_place(self, sys_request, place, expression):
        for key in sys_request.get(place):
            for pattern in self.data_files[expression]:
                match = pattern in key
                if match:
                    return False
        return True

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
                            find_one_word = 0
                            for pattern in self.data_files[expression]:
                                match = pattern in sys_request.get(place)
                                if match:
                                    find_one_word = 1
                            if not find_one_word:
                                return True
        return False
