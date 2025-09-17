from helper_functions import clear_file, append_from_file
from myabac import parse_abac_file
from acl_tools import generate_acl


def gt_acl_generator(attribute_data_file, gt_rules_file, output_file):
    
    print("running gt acl_gen")
   
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


def main():  

    attribute_data_file ="DATASETS-for-LLM/university/university-attribute-data.txt"
    gt_rules_file="llm-research/ground-truth-ABAC-rules/university-abac-rules.txt"
    output_file="llm-research/ground-truth-ACL/university-gt-ACL.txt"
    gt_acl_generator(attribute_data_file, gt_rules_file, output_file)


    return  

if __name__ == "__main__":
    main()
