from acl_tools import generate_acl, compare_acl
from helper_functions import clear_file, append_from_file
from rule import *
from myabac import parse_abac_file
from user import *

def load_rules_from_file(path: str):
    rules = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("rule"):
                rules.append(line)
    return rules

def acl_generate_single_rule(file_1, file_2):


    arr_1 = load_rules_from_file(file_1)
    arr_2 = load_rules_from_file(file_2)

    #pass in the file where we want to store the abac file that is about to be generated
    abac_file = "llm-research/session/session-abac.abac"

    #generate the abac data structures
    user, res, _  = parse_abac_file(abac_file)

    best_match ={}


    for rule1 in arr_1:
        rule_manager = RuleManager()
        rule_manager.parse_rule(rule1)
        generate_acl(user, res, rule_manager, "rule-test-1.txt")

        best_match[rule1] =("EMPTY_BY_DEFAULT", -1 )

        for rule2 in arr_2:
            rule_manager_2 = RuleManager()
            rule_manager_2.parse_rule(rule2)
            generate_acl(user, res, rule_manager_2, "rule-test-2.txt")

            _, _, _, jaccVal = compare_acl("rule-test-1.txt", "rule-test-2.txt")
  
            if jaccVal > best_match[rule1][1]:
                best_match[rule1] = (rule2, jaccVal)

    print("test1")
    for key, value in best_match.items():
        print(f"{key} => {value}\n")
    
    return



def main():  

    llm_set = "ground-truth-ABAC-rules/healthcare-abac-rules.txt"
    gt_set = "ground-truth-ABAC-rules/healthcare-abac-rules.txt"

    acl_generate_single_rule(gt_set, llm_set)
    return  

if __name__ == "__main__":
    main()


