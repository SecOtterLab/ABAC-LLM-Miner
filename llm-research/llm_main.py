from api_functions.gemini_call import gemini_api
from local_api import local_api
from helper_functions import clear_text_files, write_text_to_file, append_to_file, prepend_text_to_file, clear_file
from file_manip import move_and_rename_all
import datetime
from manual_api import manual_api
from openai_gpt5_api import openai_gpt5_api 
#stable! time 12:16 AM


def config_parser(file : str):

    execution_count = None
    max_num_it = None
    api_arr = []
    org_arr = []

 
    with open(file, "r", encoding="utf-8") as f:
        for line in f:
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue

            if stripped.startswith("execution"):
                execution_count = int(stripped.split(">")[1].strip())

            elif stripped.startswith("iteration"):
                max_num_it = int(stripped.split(">")[1].strip())

            elif stripped.startswith("api"):
                api_arr.append(stripped.split(">")[1].strip())

            elif stripped.startswith("org"):
                org_arr.append(stripped.split(">")[1].strip())


    return execution_count, max_num_it, api_arr, org_arr

def org_parser(org_line: str):
    # Expect format: "org > name(file1; file2; file3; file4)"
    org_name, rest = org_line.split("(", 1)
    org_name = org_name.replace("org >", "").strip()

    parts = rest.rstrip(")").split(";")
    parts = [p.strip() for p in parts]

         # org,          gt_acl_file,   gt_abac_rules_file, attribute_data_description_file,    attribute_data_file
    return org_name,     parts[0],      parts[1],           parts[2],                           parts[3]

def main():

    config_file = "config/config.txt"

    #clear cache and session files
    clear_text_files("llm-research/session/cache")
    clear_text_files("llm-research/session/session")
    clear_text_files("llm-research/session/output")

    try: 
  
            execution_count, max_num_it, api_arr, org_arr = config_parser(config_file)
            # print(f"APIs: {api_arr}\n")
            print(f"Organizations: {org_arr}\n")

            for api in api_arr:
                for org in org_arr:
                        


                    organization, gt_acl_file, gt_abac_rules_file, attribute_data_description_file, attribute_data_file =org_parser(str(org))


                    print(f"\n\n\nRunning {organization}...\n\n\n")


                    api_map = {
                        "gemini2.5-flash:5b" : "gemini_2_5_flash",
                        "openai-gpt5" : "openai_gpt5"
                    }
                
                    local_api_map = {
                        "deepseek-r1:70b":      {"model": "deepseek-r1:70b",      "name": "deepseek_r1_70b",      "ctx": 131072},
                        "gemma3:27b":           {"model": "gemma3:27b",           "name": "gemma3_27b",           "ctx": 131072},
                        "gpt-oss:120b":         {"model": "gpt-oss:120b",         "name": "gpt_oss_120b",         "ctx": 131072},
                        "gpt-oss:20b":          {"model": "gpt-oss:20b",          "name": "gpt_oss_20b",          "ctx": 131072},
                        "gpt-oss:latest":       {"model": "gpt-oss:latest",       "name": "gpt_oss_latest",       "ctx": 131072},
                        "llama3.1:70b":         {"model": "llama3.1:70b",         "name": "llama3_1_70b",         "ctx": 131072},
                        "llama3.3:70b":         {"model": "llama3.3:70b",         "name": "llama3_3_70b",         "ctx": 131072},
                        "llama3-gradient:70b":  {"model": "llama3-gradient:70b",  "name": "llama3_gradient_70b",  "ctx": 131072},#change back!! after testing!
                        "magistral:24b":        {"model": "magistral:24b",        "name": "magistral_24b",        "ctx": 40000},
                        "phi4-reasoning:14b":   {"model": "phi4-reasoning:14b",   "name": "phi4_reasoning_14b",   "ctx": 40000},
                        "qwen:72b":             {"model": "qwen:72b",             "name": "qwen_72b",             "ctx": 32768},
                        "qwen3:0.6b":           {"model": "qwen3:0.6b",           "name": "qwen3_0_6b",           "ctx": 1000},
                        "qwen3:32b":            {"model": "qwen3:32b",            "name": "qwen3_32b",            "ctx": 40960},
                        "reflection:70b":       {"model": "reflection:70b",       "name": "reflection_70b",       "ctx": 131072},
                    }


                   
                    


                    manual_api_map={
                        "gpt-5" :"gpt_5"
                    }

                    if api in api_map:
                        api_to_run = api_map[api]
                        model =""
                        num_ctx = 0

                    elif api in local_api_map:
                        entry = local_api_map[api]
                        api_to_run = entry["name"]
                        model = entry["model"]
                        num_ctx = entry["ctx"]

                    elif api in manual_api_map:
                        api_to_run = manual_api_map[api]
                        model =""
                        num_ctx = 0
                    else:
                        raise SystemExit(f"Unknown API: {api}")
                    

                    for i in range(execution_count):
                        print(f"Run: {i}...")
                        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                        meta_data = (
                            f"# org : {organization}{timestamp}\n"
                            f"# iterations : {max_num_it}\n"
                            f"# api_called : {api}\n"
                            f"# gt_file : {gt_acl_file}\n"
                            f"# gt_abac_rule_file : {gt_abac_rules_file}\n"
                            f"# attribute_data_description_file : {attribute_data_description_file}\n"
                            f"# attribute_data_file : {attribute_data_file}\n"
                        )
                        stats_text = (f"# org : {organization}, LLM : {api_to_run}, num_ctx : {num_ctx}")
                        append_to_file( "llm-research/session/output/statistics.txt", stats_text )


                        if api_to_run == "gemini_2_5_flash":
                            gemini_api( gt_acl_file, gt_abac_rules_file, attribute_data_file, attribute_data_description_file, max_num_it, None, None)
                        elif api_to_run == "openai_gpt5":
                            openai_gpt5_api( gt_acl_file, gt_abac_rules_file, attribute_data_file, attribute_data_description_file, max_num_it, None, None)
                        elif api in local_api_map:
                            local_api( gt_acl_file, gt_abac_rules_file, attribute_data_file, attribute_data_description_file, max_num_it, model, num_ctx) #add name of api for this call!!!!
                        elif api_to_run in manual_api_map.values():
                            manual_api( gt_acl_file, gt_abac_rules_file, attribute_data_file, attribute_data_description_file, max_num_it, None, None)
                        else:
                            print(f"API is not assigned a function: {api}") 

                        # Save all session files and cache files generated from the session 
                        
                        session_info = "llm-research/session/session/session-info.txt" 
                        write_text_to_file(session_info, meta_data)
                        move_and_rename_all("llm-research/session", f"tracebook/{organization}/{api_to_run}" , organization, timestamp)
                        move_and_rename_all("llm-research/session/output", f"output/{organization}/{api_to_run}", organization, timestamp)

                        clear_text_files("llm-research/session/cache")
                        clear_text_files("llm-research/session/session")
                        clear_text_files("llm-research/session/output")
                        clear_file("prompts/complete-prompt.txt")


                        # clear cache and session files

    except:
        prepend_text_to_file("llm-research/session/cache/statistics.cache",f"Error config file is misconfigured\n")
   
        clear_text_files("llm-research/session/cache")
        clear_text_files("llm-research/session/session")
        clear_text_files("llm-research/session/output")
        clear_file("prompts/complete-prompt.txt")


        return
    

if __name__ == "__main__":
    main()





