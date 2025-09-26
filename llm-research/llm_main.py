from api_functions.gemini_call import gemini_api
from local_api import local_api
from helper_functions import clear_text_files, write_text_to_file, append_to_file
from file_manip import move_and_rename_all
import datetime
from manual_api import manual_api
from openai_gpt5_api import openai_gpt5_api 

class ContinueOuter(Exception):
    """Signal to skip to the next outer-loop iteration."""
    pass

def main():
    config_file = "config/config.txt"

    #clear cache and session files
    clear_text_files("llm-research/session/cache")
    clear_text_files("llm-research/session/session")
    clear_text_files("llm-research/session/output")

   
    with open(config_file, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip() and not line.startswith("#")]

        execution_count = int(lines[0])
        max_num_it = int(lines[1])
        api_name = lines[2]

        for org_line in lines[3:]:
            org_name, rest = org_line.split("(", 1)
            org_name = org_name.strip()
            parts = rest.rstrip(")").split(";")
            parts = [p.strip() for p in parts]

            organization = org_name
            gt_acl_file = parts[0]
            gt_abac_rules_file = parts[1]
            attribute_data_description_file = parts[2]
            attribute_data_file = parts[3]


    api_map = {
        "gemini2.5-flash:5b" : "gemini_2_5_flash",
        "openai-gpt5" : "openai_gpt5"
    }
    local_api_map = {
        "gemini2.5-flash:5b" : "gemini_2_5_flash",
        "deepseek-1:70b": "deepseek_r1_70b",
        "gpt-oss:120b": "gpt_oss_120b",
        "llama3.1:70b": "llama3_1_70b",
        "llama3.3:70b": "llama3_3_70b",
        "qwen:72b": "qwen_72b",
        "reflection:70b": "reflection_70b"
    }

    manual_api_map={
        "gpt-5" :"gpt_5"
    }

    if api_name in api_map:
        api_to_run = api_map[api_name]

    elif api_name in local_api_map:
        api_to_run = local_api_map[api_name]

    elif api_name in manual_api_map:
        api_to_run = manual_api_map[api_name]
    else:
        raise SystemExit(f"Unknown API: {api_name}")



    for i in range(execution_count):
        print(f"Run: {i}...")
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        meta_data = (
            f"# org : {organization}{timestamp}\n"
            f"# iterations : {max_num_it}\n"
            f"# api_called : {api_name}\n"
            f"# gt_file : {gt_acl_file}\n"
            f"# gt_abac_rule_file : {gt_abac_rules_file}\n"
            f"# attribute_data_description_file : {attribute_data_description_file}\n"
            f"# attribute_data_file : {attribute_data_file}\n"
        )
        stats_text = (f"# org : {organization}, LLM : {api_to_run}")
        append_to_file( "llm-research/session/output/statistics.txt", stats_text )


        if api_to_run == "gemini_2_5_flash":
            gemini_api( gt_acl_file, gt_abac_rules_file, attribute_data_file, attribute_data_description_file, max_num_it)
        elif api_to_run == "openai_gpt5":
            openai_gpt5_api( gt_acl_file, gt_abac_rules_file, attribute_data_file, attribute_data_description_file, max_num_it)
        elif api_to_run in local_api_map.values():
            local_api( gt_acl_file, gt_abac_rules_file, attribute_data_file, attribute_data_description_file, max_num_it)
        elif api_to_run in manual_api_map.values():
            manual_api( gt_acl_file, gt_abac_rules_file, attribute_data_file, attribute_data_description_file, max_num_it)
        else:
            raise SystemExit(f"API is not assigned a function: {api_name}") 

        # Save all session files and cache files generated from the session 
        
        session_info = "llm-research/session/session/session-info.txt" 
        write_text_to_file(session_info, meta_data)
        move_and_rename_all("llm-research/session", f"tracebook/{org_name}/{api_to_run}" , org_name, timestamp)
        move_and_rename_all("llm-research/session/output", f"output/{org_name}/{api_to_run}", org_name, timestamp)

        clear_text_files("llm-research/session/cache")
        clear_text_files("llm-research/session/session")
        clear_text_files("llm-research/session/output")

        #clear cache and session files
        

    return
    

if __name__ == "__main__":
    main()





