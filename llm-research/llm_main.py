from api_functions.gemini_call import gemini_api
from helper_functions import clear_text_files, write_text_to_file
from file_manip import move_and_rename_all
import datetime

def parse_config_file(file):
    with open(file, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip() and not line.startswith("#")]


    max_iterations = int(lines[0])
    api_to_run = lines[1]

    for org_line in lines[2:]:
        org_name, rest = org_line.split("(", 1)
        org_name = org_name.strip()
        parts = rest.rstrip(")").split(";")
        parts = [p.strip() for p in parts]

        organization = org_name
        ground_truth_acl = parts[0]
        ground_truth_abac_rules = parts[1]
        attribute_data_description = parts[2]
        attribute_data = parts[3]
        output_dir = parts[4]


        print(f"{max_iterations}\n{api_to_run}\n{organization}\n{ground_truth_acl}\n{ground_truth_abac_rules}\n{attribute_data_description}\n{attribute_data}\n{output_dir}\n")
        
    return



def main():
    config_file = "config/config.txt"

    #clear cache and session files
    clear_text_files("llm-research/session/cache")
    clear_text_files("llm-research/session")

   
    with open(config_file, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip() and not line.startswith("#")]

        max_num_it = int(lines[0])
        api_to_run = lines[1]

        for org_line in lines[2:]:
            org_name, rest = org_line.split("(", 1)
            org_name = org_name.strip()
            parts = rest.rstrip(")").split(";")
            parts = [p.strip() for p in parts]

            organization = org_name
            gt_acl_file = parts[0]
            gt_abac_rules_file = parts[1]
            attribute_data_description_file = parts[2]
            attribute_data_file = parts[3]
            tracebook_path = parts[4]
            output_path = parts[5]


            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            meta_data = (f"{org_name}{timestamp}\n{max_num_it}\n{api_to_run}\n{organization}\n{gt_acl_file}\n{gt_abac_rules_file}\n{attribute_data_description_file}\n{attribute_data_file}\n{tracebook_path}\n{output_path}\n")


            # A call to any API should be made here
            gemini_api( gt_acl_file, attribute_data_file, attribute_data_description_file, max_num_it)

            #TODO: generate analytics here

            # Save all session files and cache files generated from the session 
            
            session_info = "llm-research/session/session-info.txt"
            write_text_to_file(session_info, meta_data)
            move_and_rename_all("llm-research/session", tracebook_path , org_name, timestamp)
            move_and_rename_all("llm-research/session/output", output_path , org_name, timestamp)


            clear_text_files("llm-research/session/cache")
            clear_text_files("llm-research/session")

    return
   

    





if __name__ == "__main__":
    main()





