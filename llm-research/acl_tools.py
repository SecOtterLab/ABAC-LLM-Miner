from rule import *
from myabac import parse_abac_file
from user import *
from helper_functions import *
#function to traverse a file (ACL files) and store lines in a set to compare
#Snipets of code taken from core.myabac generate_heatmap_data

def compare_acl (acl1, acl2):

    try: 
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
    
    except Exception as e:
        
        gt_acl_count =  count_lines(acl1)
         
        stats_text = (f"\n  acl_jacc_val : {0},"
                    f"\n  gt_acl : {gt_acl_count},"
                    f"\n  llm_acl : {0},"
                    f"\n  intersection : {0},"
                    f"\n  under_perm : {gt_acl_count},"
                    f"\n  over_perm : {0},")
         
        prepend_text_to_file("llm-research/session/cache/statistics.cache", f"Error in acl_tools.compare_acl{e}")
        return stats_text, ["empty"], False, 0.0
    
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

    try:
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

        return
    except Exception as e:
        prepend_text_to_file("llm-research/session/cache/statistics.cache", f"Error in acl_tools.generate_acl: {e}")

        return
    
def rule_semantic_analyzer(file_1, file_2, attribute_data_file):

    try: 
        arr_1 = load_rules_from_file(file_1)
        arr_2 = load_rules_from_file(file_2)
        
        if file_to_text("llm-research/session/session/session-ACL.txt").strip() =="":
            return 0, {}

        if not arr_1 or not arr_2:
            return 0, {}
        
        
        #pass in the file where we want to store the abac file that is about to be generated

        #generate the abac data structures
        user, res, _  = parse_abac_file(attribute_data_file)
        jacc_total = 0

        best_match ={}

        for rule1 in arr_1:
            rule_manager = RuleManager()
            try:
                rule_manager.parse_rule(rule1)
                
            except:
                rule_manager.parse_rule("rule(<malForm> ; <malForm> ; <malForm> ; <malForm> )")

            generate_acl(user, res, rule_manager, "llm-research/session/session/session-ACL-single-rule-file-1.txt")
            
            temp_string = (f"\n{rule1}"
                            # f"\n{file_to_text("llm-research/session/session/session-ACL-single-rule-file-1.txt")}"
                            f"\n{file_to_text('llm-research/session/session/session-ACL-single-rule-file-1.txt')}"

                            f"\n===============================================\n"
                        )
            append_to_file("llm-research/session/cache/per_rule_acl.cache", temp_string)

            best_match[rule1] =("EMPTY_BY_DEFAULT", 0 )

            for rule2 in arr_2:
                rule_manager_2 = RuleManager()
                try:
                    rule_manager_2.parse_rule(rule2)
                except:
                    rule_manager_2.parse_rule("rule(<malForm> ; <malForm> ; <malForm> ; <malForm> )")

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
    

    except Exception as e:
        prepend_text_to_file("llm-research/session/cache/statistics.cache", f"Error in acl_tools.rule_semantic_analyzer: {e}")
        return 0.0, {}
    
def jaccard(set1, set2):

    s1, s2 = set(set1), set(set2)

    intersection = len(s1 & s2)
    union = len(s1 | s2)

    if union <= 0:
        return 0

    jacc_value = float(intersection / union)
    return jacc_value

def gt_acl_generator(attribute_data_file, gt_rules_file, output_file):
    try:
        print("running gt acl_gen...")
    
        #pass in the file where we want to store the abac file that is about to be generated
        abac_file = "llm-research/session/session-abac.abac"

        clear_file(abac_file)

        #combine the attribute data file with the gt rules to make an abac file
        append_from_file(abac_file, attribute_data_file)
        append_from_file(abac_file, gt_rules_file)

        #generate the abac data structures
        user, res, rule = parse_abac_file(abac_file)

        #generate the acl
        generate_acl(user, res, rule, output_file)

        return
    except Exception as e:
        prepend_text_to_file("llm-research/session/cache/statistics.cache", f"Error in ground_truth_ACL_generator.gt_acl_generator: {e}")

        return

def main():  
    #   Permission counts: per Dr.Buis previous work on https://dl.acm.org/doi/abs/10.1145/3734436.3734441
    #   edocument           :   32961
    #   healthcare          :   43
    #   project-management  :   101
    #   university          :   168
    #   workforce           :   15858    


    # # edocument
    # attribute_data_file = "DATASETS-for-LLM/edocument/edocument-attribute-data.txt"
    # gt_rules_file = "ground-truth-ABAC-rules/edocument-abac-rules.txt"
    # output_file = "ground-truth-ACL/edocument-gt-ACL.txt"
    # gt_acl_generator(attribute_data_file, gt_rules_file, output_file)


    # # healthcare
    # attribute_data_file = "DATASETS-for-LLM/healthcare/healthcare-attribute-data.txt"
    # gt_rules_file = "ground-truth-ABAC-rules/healthcare-abac-rules.txt"
    # output_file = "ground-truth-ACL/healthcare-gt-ACL.txt"
    # gt_acl_generator(attribute_data_file, gt_rules_file, output_file)

    # # project-management
    # attribute_data_file = "DATASETS-for-LLM/project-management/project-management-attribute-data.txt"
    # gt_rules_file = "ground-truth-ABAC-rules/project-management-abac-rules.txt"
    # output_file = "ground-truth-ACL/project-management-gt-ACL.txt"
    # gt_acl_generator(attribute_data_file, gt_rules_file, output_file)

    # # university
    # attribute_data_file = "DATASETS-for-LLM/university/university-attribute-data.txt"
    # gt_rules_file = "ground-truth-ABAC-rules/university-abac-rules.txt"
    # output_file = "ground-truth-ACL/university-gt-ACL.txt"
    # gt_acl_generator(attribute_data_file, gt_rules_file, output_file)

    # # workforce
    # attribute_data_file = "DATASETS-for-LLM/workforce/workforce-attribute-data.txt"
    # gt_rules_file = "ground-truth-ABAC-rules/workforce-abac-rules.txt"
    # output_file = "ground-truth-ACL/workforce-gt-ACL.txt"
    # gt_acl_generator(attribute_data_file, gt_rules_file, output_file)




    return  

if __name__ == "__main__":
    main()
