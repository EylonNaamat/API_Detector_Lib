import os
import re
from .SYS_Rule import SYS_Rule
from .SYS_Operators import SYS_Operators
from .SYS_Request import SYS_Request
"""
this is the class you will use for using the system
this is the main class that concentrate all the other classes and will connect between them for making the prediction
it will load the rules from the conf files into list of SYS_Rules and create the logic part of SYS_Operators object 
and by using the function detect_malicious_request that get a request it will check it and return if it is 
malware or benign
"""
class API_Detector:
    def __init__(self, rules_folder):
        self.rules_folder = rules_folder
        self.rules = []
        self.rule_executor = SYS_Operators()
        self.good_operators = ["@rx", "@pmFromFile", "!@rx", "!@pmFromFile","@contains", "!@contains","@ipMatch", "@pm","!@pm", "@eq","!@eq", "@endsWith"]
        self.good_places = [
            "REQUEST_LINE",
            "ARGS_NAMES",
            "FILES_NAMES",
            "REQUEST_COOKIES",
            "!REQUEST_COOKIES",
            "ARGS_GET",
            "FILES",
            "REQUEST_HEADERS",
            "!REQUEST_HEADERS",
            "REQUEST_FILENAME",
            "ARGS",
            "REQUEST_PROTOCOL",
            "REQUEST_BODY",
            "ARGS_GET_NAMES",
            "QUERY_STRING",
            "REQBODY_PROCESSOR",
            "REQUEST_METHOD",
            "REMOTE_ADDR",
            "REQUEST_URI_RAW",
            "REQUEST_URI",
            "REQUEST_BASENAME",
            "UNIQUE_ID",
            "REQUEST_HEADERS_NAMES"
        ]
        self.load_rules()

    # split the content by |to get the places we need to check for the condition
    # and check that the place is in the good_place list
    #str->[str]
    def extract_place_to_lookfor(self, content: str):
        places = content.split('|')
        ans = []
        for place in places:
            if place.split(':')[0] in self.good_places:
                ans.append(place)
        return ans

    # return operator and the args for it
    # if the string not contain space there is no args return Nune
    #str->[oper,args]
    def extract_operator_and_args(self, content: str):
        ans = []
        try:
            space_index = content.index(' ')
            ans.append(content[:space_index])
            ans.append(content[space_index+1:])
        except:
            ans.append(content)
            ans.append(None)

        return ans

    # extract the extra information from the rule
    # str -> {str:str}
    def get_extra_information(self,content: str):
        # extra_info is dict that will save the answer
        extra_info = {}

        # split the content to list
        rule =[]
        if content != 'chain':
            # get the rule and split in its components from id to the end
            rule = (content or "").strip().strip(',').split(',')
            for index, val in enumerate(rule):
                if val.startswith("id:"):
                    continue
                rule[index] = rule[index].lstrip(' ')
        else:
            rule.append(content)
        # get the action filed
        if "pass" in rule:
            extra_info['action'] = "pass"
        else:
            extra_info['action'] = "block"


        # get the id
        ids = [piece for piece in rule if piece.startswith("id:")]
        if len(ids) >= 1:
            extra_info['id']=ids[0].replace('id:', '')
        else:
            extra_info['id'] = None

        # get the msg
        msgs = [piece for piece in rule if piece.startswith("msg:")]
        if len(msgs) >= 1 :
            extra_info['msg'] = msgs[0].replace('msg:', '')
        else:
            extra_info['msg'] = None


        # get the tags
        tags = [piece for piece in rule if piece.startswith("tag:")]

        for index, val in enumerate(tags):
            tags[index] = val.replace('tag:', '')

        extra_info['tags'] = tags

        # get the severitys
        severitys = [piece for piece in rule if piece.startswith("severity:")]
        if len(severitys) >= 1:
            extra_info['severity'] = severitys[0].replace('severity:', '')
        else:
            extra_info['severity'] = None

        # check if has child
        if "chain" in rule:
            extra_info['chain'] = True
        else:
            extra_info['chain'] = False

        return extra_info

    # this function read all the rules from the .conf file and place it in the rules list
    def load_rules(self):
        # list of all the ids in the files use to check there are no 2 rules with same id
        seen_ids = set()

        # list of all the .conf file rules_folder
        rule_files = [f for f in os.listdir(self.rules_folder) if f.endswith('.conf')]

        # run on all the files
        for rulefile in rule_files:
            # read the content
            rule_file_path = os.path.join(self.rules_folder, rulefile)
            with open(rule_file_path, 'r') as f:
                content = f.read()
            #use for debugging
            lineno = 0

            # this variable help as to find rules that depend on other rules (has child rule)
            this_chained = next_chained = False

            # use to save the previous line for conacting line together
            prevline = None

            # for each line in the rule file
            for line in content.splitlines():
                lineno += 1
                # handle continuation lines
                line = (prevline + line) if prevline else line

                # remove comments from line
                line = re.sub(r'(^([^\'"]|\'[^\']+\'|"[^"]+\'|"[^"]+")#).*', r'\1', line)

                # replace the "\" with space
                if line.endswith('\\'):
                    # change the last one to space and pass to the next line
                    prevline = line[:-1] + " "
                    continue
                else:
                    prevline = None

                # skip if it's an empty line (this also skip comment-only lines)
                if re.match(r'(?:^\s+$|^#)', line):
                    continue

                # remember if this line is chained to the previous or not
                this_chained = next_chained
                next_chained = False

                # split the directive in its components, considering quoted strings
                directive = re.findall(
                    r'([^\'"\s][^\s]*[^\'"\s]|\'(?:[^\']|\\\')*[^\']\'|"(?:[^"]|\\")*[^\\]")(?:\s+|$)', line)
                directive = [piece[1:-1] if (piece[0] == '"' or piece[0] == "'") else piece for piece in directive]

                # skip if it's not a SecRule or SecAction
                if len(directive) and directive[0] == "SecRule":
                    if directive[1] == 'TX:DETECTION_PARANOIA_LEVEL':
                        continue
                else:
                    continue

                # add empty values for the list to get length > 3
                while len(directive)<4:
                    directive.append("")


                # extract the information from the directive for the Rule class
                place_to_lookfor = self.extract_place_to_lookfor(directive[1])
                operator , args = self.extract_operator_and_args(directive[2])
                extra_info = self.get_extra_information(directive[3])

                # remember that the next rule is child rule
                next_chained = extra_info['chain']

                # make new Rule
                curr_rule = SYS_Rule(place_to_lookfor,operator,args,extra_info)

                # if the rule is a child rule we add it as a child and if not we add it to the rule list
                if this_chained:
                    self.rules[-1].add_child_rule(curr_rule)
                else:
                    if curr_rule.id in seen_ids:
                        print(f"{rulefile}:{lineno} rule with duplicate id {curr_rule.id}")
                    else:
                        seen_ids.add(curr_rule.id)
                        self.rules.append(curr_rule)

        # take off all the rule which not appears in the good_operators list
        new_rule_list =[]
        for index, value in enumerate(self.rules):
            check_rule = value
            check_flag = True
            while check_rule is not None:
                if check_rule.operator not in self.good_operators:
                    check_flag = False
                check_rule = check_rule.child_rule

            if check_flag:
                new_rule_list.append(value)

        # update the new list in to the class list
        self.rules = new_rule_list


    async def detect_malicious_request(self, request, request_type):
        req = SYS_Request()
        await req.fill(request, request_type)
        for rule in self.rules:
            if self.rule_executor.exec(rule, req):
                return True
        return False





