# import ollama
from helper_functions import iterate_api_requests
from helper_functions import file_to_text
import re
import subprocess


#NOTE: We clear all data from GPT or manual models before running them.
#   this is to simulate a API call that would not retain previous chats in memory 
def manual_api(gt_acl_file, gt_abac_rules_file, attribute_data_file, attribute_data_description_file, max_num_it, model, num_ctx):

    iterate_api_requests(gt_acl_file, gt_abac_rules_file, attribute_data_file, attribute_data_description_file, max_num_it, manual_api_call, model, num_ctx)
    return

def strip_backslashes_from_file(filepath: str) -> None:
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    cleaned = content.replace("\\", "")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(cleaned)




def ignore_verbose_response(resp : str) -> str:
    try:
        pattern = r"rule\(.*?\)" # . = all characters , * repeats for all until it hits ), ? stops at the first ')'
        
        str_arr = re.findall(pattern, resp)
        str_builder = ""

        for rule in str_arr:
            str_builder +=f"{rule.strip()}\n"

        return str_builder
    except:
        print("error in verbose")
        return "error"


def manual_api_call(request_text):
    
    print(f"Copy text from: prompts/complete-prompt.txt\n Every iteration WILL have a unique prompt\n")
    input_confirm = input (f"Paste in response to the manual-input.txt and type 'd' when done\n>>$")

    if input_confirm !='d': 
        print(f"ERROR: input rules and try again\n")
        return    
    
    subprocess.run(['open', '-a','Spotify'])

    strip_backslashes_from_file("ignore/manual-input.txt")
    final_string = file_to_text("ignore/manual-input.txt")
    
    print(final_string)

    final_string = ignore_verbose_response(final_string)
    print("------------------------------------------------")
    print(final_string)

    


    return str(final_string)



def main():
    manual_api_call("nothign")

if __name__ == "__main__":
    main()

