import sys
from user import UserManager
from res import ResourceManager
from rule import RuleManager

def parse_abac_file(filename):
    """
    Delegate parsing based on what line contains (user, resource, or rule)

    Args:
        filename (str): path to file

    Returns:
        UserManager, ResourceManager, RuleManager: initalized objects poulated based on parsed abac
    """
    user_mgr = UserManager()
    res_mgr = ResourceManager()
    rule_mgr = RuleManager()

    with open(filename, 'r', encoding="UTF-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            if line.startswith('userAttrib'):
                user_mgr.parse_user_attrib(line)
            elif line.startswith('resourceAttrib'):
                res_mgr.parse_resource_attrib(line)
            elif line.startswith('rule'):
                rule_mgr.parse_rule(line)

    return user_mgr, res_mgr, rule_mgr

def process_request(request, user_mgr, res_mgr, rule_mgr):
    """
    Given a request in the form "<user>, <resource>, <action>" the function

    Args:
        request (str): request string to be evaluated
        user_mgr (UserManager): holds user data from abac
        res_mgr (ResourceManager): holds resources from abac
        rule_mgr (RuleManager): holds rules from abac

    Returns:
        str: 'Permit' or 'Deny'
    """
    sub_id, res_id, action = request.strip().split(',')

    user = user_mgr.get_user(sub_id)
    resource = res_mgr.get_resource(res_id)

    if not user or not resource:
        return "Deny"

    # Check if any rule permits the action
    for rule in rule_mgr.rules:
        if rule.evaluate(user, resource, action):
            return "Permit"

    return "Deny"







def main():
    # if len(sys.argv) > 4 or (sys.argv[1] not in ['-e', '-a', '-b']):
    #     print("Usage: for request file evaluation python3 myabac.py -e <policy_file> <request_file>\n")
    #     print("for policy file analysis use  python3 myabac.py -a <policy_file> ")
    #     print("for resources analysis use  python3 myabac.py -b <policy_file> ")
    #     sys.exit(1)

    # policy_file = sys.argv[2]

    # # Parse the policy file
    # user_mgr, res_mgr, rule_mgr = parse_abac_file(policy_file)

    # if sys.argv[1] == "-e":
    #     request_file = sys.argv[3]
    # # Process requests
    #     with open(request_file, 'r', encoding="UTF-8") as f:
    #         for line in f:
    #             line = line.strip()
    #             if not line or line.startswith('#'):
    #                 continue

    #             decision = process_request(line, user_mgr, res_mgr, rule_mgr)
    #             print(f"{line}: {decision}")

    # if sys.argv[1]=="-a":
    #     heatmap = generate_heatmap_data(user_mgr, res_mgr, rule_mgr)
    #     visualize_heatmap(heatmap)
 

    # if sys.argv[1]=="-b":
    #     top10, least10 = generate_bar_data(user_mgr, res_mgr, rule_mgr)
    #     plot_bar_data(top10, least10)

# if __name__ == "__main__":
#     main()
    pass