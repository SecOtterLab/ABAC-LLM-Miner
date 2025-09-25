from rule import *
from myabac import parse_abac_file
from user import *


#function to traverse a file (ACL files) and store lines in a set to compare
def file_to_set(file_name):
    
    lines =  set()

    with open (file_name, "r", encoding="utf-8") as f:
        for line in f:
            lines.add(line.strip())
    return lines


def load_rules_from_file(path: str):
    rules = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("rule"):
                rules.append(line)
    return rules


def file_to_text(filename):
    temp_string = ""

    with open (filename, "r", encoding="utf-8") as f:
        temp_string += f.read().strip()
    
    return temp_string


def append_to_file(filename, text):
    with open(filename, "a", encoding="utf-8") as f:
        f.write(str(text))

    return


def compare_acl (acl1, acl2):

    acl1 = file_to_set(acl1)
    acl2 = file_to_set(acl2)

    common = acl1 & acl2
    only_in_acl1  = acl1 - acl2
    only_in_acl2  = acl2 - acl1

    lines = []
    lines.append(f"Commong lines / Lines that are correct: {len(common)}")
    lines.extend(sorted(common))
    lines.append("")
    lines.append(f"Only in ACL 1 (under permissions): {len(only_in_acl1)}")
    lines.extend(sorted(only_in_acl1))
    lines.append("")
    lines.append(f"Only in ACL 2 (over permissions): {len(only_in_acl2)}")
    lines.extend(sorted(only_in_acl2))
    lines.append("")
    lines.append(f"Total different lines: {len(only_in_acl1 ^ only_in_acl2)}")

    jacc_val = jaccard(acl1 , acl2)

    stats_text = (f"\n  acl_jacc_val : {jacc_val},"
                  f"\n  gt_acl : {len(acl1)},"
                  f"\n  llm_acl : {len(acl2)},"
                  f"\n  intersection : {len(common)},"
                  f"\n  under_perm : {len(only_in_acl1)},"
                  f"\n  over_perm : {len(only_in_acl2)},")
    # print(stats_text)

    #if there is a 100% match then lists that have unique ACL line will return true
    complete_match = False
    if(jacc_val > .98):
        complete_match = True

    return stats_text, lines, complete_match, jacc_val


#Snipets of code taken from core.myabac generate_heatmap_data

def generate_acl(user_mgr, res_mgr, rule_mgr, output_file):

    #Arguements should be the return data structures of core.myabac parse_abac_file
    """
    Perform rule analysis and produce a heatmap  

    Arguments:
        user_mgr (UserManager): Manages users and their attributes.
        res_mgr (ResourceManager): Manages resources and their attributes.
        rule_mgr (RuleManager): Manages rules for authorization.

    Returns:
        None
        Creates a .txt file with the ACL of the corresponding file
    """
    all_actions = set()
    seen  = set()
    #access all the actions in rule.mngr
    for rule in rule_mgr.rules:
        all_actions.update(rule.acts)

    # print (all_actions)
    i = 0
    # Prepare attribute mappings and rule coverage
    for rule_idx, rule in enumerate(rule_mgr.rules):
        rule_attributes = rule.get_attributes()

        # Evaluate rule over all users and resources
        # Nested loops
        # check every uid in user_mngr
        #   against every rid in rid_manager
        #       against every action in rule_mngr ()
        for uid, user in user_mgr.users.items():
            for rid, resource in res_mgr.resources.items():
                for action in all_actions:
                    if rule.evaluate(user, resource, action) :
                        temp_string = (f"{uid}, {rid}, {action}")

                        if temp_string not in seen:
                            seen.add(temp_string)
                            i += 1
                            # print(f"{i}. {temp_string} ")

    with open(output_file, "w", encoding="utf-8") as f:
        for line in seen:
            f.write(line +"\n")


    # print(f"permission Count {i}")

    return


def rule_semantic_analyzer(file_1, file_2, attribute_data_file):


    arr_1 = load_rules_from_file(file_1)
    arr_2 = load_rules_from_file(file_2)

    #pass in the file where we want to store the abac file that is about to be generated

    #generate the abac data structures
    user, res, _  = parse_abac_file(attribute_data_file)
    jacc_total = 0

    best_match ={}

    for rule1 in arr_1:
        rule_manager = RuleManager()
        rule_manager.parse_rule(rule1)
        generate_acl(user, res, rule_manager, "llm-research/session/session/session-ACL-single-rule-file-1.txt")
        
        temp_string = (f"\n{rule1}"
                        f"\n{file_to_text("llm-research/session/session/session-ACL-single-rule-file-1.txt")}"
                        f"\n===============================================\n"
                    )
        append_to_file("llm-research/session/cache/per_rule_acl.cache", temp_string)

        best_match[rule1] =("EMPTY_BY_DEFAULT", -1 )

        for rule2 in arr_2:
            rule_manager_2 = RuleManager()
            rule_manager_2.parse_rule(rule2)
            generate_acl(user, res, rule_manager_2, "llm-research/session/session/session-ACL-single-rule-file-2.txt")

            _, _, _, jaccVal = compare_acl("llm-research/session/session/session-ACL-single-rule-file-1.txt", "llm-research/session/session/session-ACL-single-rule-file-2.txt")

        
            if jaccVal > best_match[rule1][1]:
                best_match[rule1] = (rule2, jaccVal)
        #TODO: make session folders for the files above
    for key, value in best_match.items():
        # print(f"{key} => {value}\n")
        jacc_total += value[1]

    jacc_avg = jacc_total / len(best_match)

    # print(f"TOTAL JACC  AVG: {jacc_avg}")
    return jacc_avg, best_match


def jaccard(set1, set2):

    s1, s2 = set(set1), set(set2)

    intersection = len(s1 & s2)
    union = len(s1 | s2)

    if union <= 0:
        return 0

    jacc_value = float(intersection / union)
    return jacc_value



def main():

    # gt_set = file_to_set("ground-truth-ACL/healthcare-gt-ACL.txt")
    # llm_set = file_to_set("jaccard-testing-ACL.txt")
    # val = ((jaccard(gt_set,llm_set)))
    # compare_acl("ground-truth-ACL/healthcare-gt-ACL.txt", "jaccard-testing-ACL.txt")
    
    # print(repr(val))

    # rule_semantic_analyzer("ground-truth-ABAC-rules/healthcare-abac-rules.txt", "ground-truth-ABAC-rules/healthcare-abac-rules.txt")

    return

if __name__ == "__main__":
    main()