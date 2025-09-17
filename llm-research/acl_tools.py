#function to traverse a file (ACL files) and store lines in a set to compare
def file_to_set(file_name):
    
    lines =  set()

    with open (file_name, "r", encoding="utf-8") as f:
        for line in f:
            lines.add(line.strip())
    return lines

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
    lines.append(f"Only in ground truth ACL (under permissions): {len(only_in_acl1)}")
    lines.extend(sorted(only_in_acl1))
    lines.append("")
    lines.append(f"Only in LLM ACL (over permissions): {len(only_in_acl2)}")
    lines.extend(sorted(only_in_acl2))
    lines.append("")
    lines.append(f"Total different lines: {len(only_in_acl1 ^ only_in_acl2)}")

    #if there is a 100% match then lists that have unique ACL line will return true
    complete_match = False
    if((len(acl1) == 0 and len(only_in_acl2) == 0) and (len(acl1) == len(acl2))):
        complete_match = True

    return lines, complete_match


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


    print(f"permission Count {i}")

    return



