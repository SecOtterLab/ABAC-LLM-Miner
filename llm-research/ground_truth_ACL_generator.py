from helper_functions import clear_file, append_from_file, prepend_text_to_file
from myabac import parse_abac_file
from acl_tools import generate_acl


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
