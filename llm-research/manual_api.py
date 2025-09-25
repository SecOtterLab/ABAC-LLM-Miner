# import ollama
from helper_functions import iterate_api_requests
from helper_functions import file_to_text


#NOTE: We clear all data from GPT or manual models before running them.
#   this is to simulate a API call that would not retain previous chats in memory 
def manual_api(gt_acl_file, gt_abac_rules_file, attribute_data_file, attribute_data_description_file, max_num_it):

    iterate_api_requests(gt_acl_file, gt_abac_rules_file, attribute_data_file, attribute_data_description_file, max_num_it, manual_api_call)
    return

def strip_backslashes_from_file(filepath: str) -> None:
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    cleaned = content.replace("\\", "")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(cleaned)

def read_in_chunks(filepath, chunk_size=3800):
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()
        for i in range(0, len(text), chunk_size):
            print(text[i:i+chunk_size])
            if i + chunk_size < len(text):
                print("=======================================================================================")
                print(f"Read this prompt keep it in memory and i will tell you when to execute the entire prompts I have given you.\n this is only part of the prompt just broken down to meet your input size\n")
                input("\nPress Enter to continue...\n")

def manual_api_call(request_text):
    
    # print(f"Copy text from: prompts/complete-prompt.txt\n Every iteration WILL have a unique prompt\n")
    # input_confirm = input (f"Paste in response to the manual-input.txt and type 'd' when done\n>>$")

    # if input_confirm !='d': 
    #     print(f"ERROR: input rules and try again\n")
    #     return

    read_in_chunks("prompts/complete-prompt.txt")
    


    strip_backslashes_from_file("manual-input.txt")
    final_string = file_to_text("manual-input.txt")
 
    return str(final_string)



# def main():
#     local_api_call()

# if __name__ == "__main__":
#     main()

