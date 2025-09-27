# import ollama
import requests
import re
from helper_functions import iterate_api_requests, prepend_text_to_file
# import sys
# from ollama import chat
# from ollama import ChatResponse
from ollama import Client
# import subprocess

#READ ME:
    # To run one must be hosting the right LLM on ollama 
    # our url is not avialble to users with an ip not in our white list
    # LLMs with a context window large enough and available to us are the following:
        # reflection:70b        5084e77c1e10    39 GB     45 hours ago    context length      131072   
        # llama3.3:70b          a6eb4748fd29    42 GB     46 hours ago    context length      131072
        # gpt-oss:120b          f7f8e2f8f4e0    65 GB     2 weeks ago     
        # deepseek-r1:70b       d37b54d01a76    42 GB     2 weeks ago     
        # llama3.1:70b          711a9e8463af    42 GB     3 weeks ago     

    #LLMs available through our server (smaller LLMs do not have a context window large enough to reason)
        # reflection:70b        5084e77c1e10    39 GB     45 hours ago    context length      131,072     
        # llama3.3:70b          a6eb4748fd29    42 GB     46 hours ago    context length      131,072 
        # qwen:72b              e1c64582de5c    41 GB     2 days ago      context length      32,768 
        # gemma3:27b            a418f5838eaf    17 GB     3 days ago      context length      131,072 
        # magistral:24b         27bcbbf6d324    14 GB     3 days ago      context length      40,000 
        # phi4-reasoning:14b    47e2630ccbcd    11 GB     3 days ago      context length      40,000 
        # gpt-oss:120b          f7f8e2f8f4e0    65 GB     2 weeks ago     context length      131,072
        # deepseek-r1:70b       d37b54d01a76    42 GB     2 weeks ago     context length      131,072  
        # gpt-oss:latest        aa4295ac10c3    13 GB     2 weeks ago     context length      131,072  
        # llama3.1:70b          711a9e8463af    42 GB     3 weeks ago     context length      131,072 
        # qwen3:32b             030ee887880f    20 GB     3 weeks ago     context length      40,960 
        # gpt-oss:20b           aa4295ac10c3    13 GB     3 weeks ago     context length      131,072
        # qwen3:0.6b            7df6b6e09427    522 MB    3 weeks ago     context length      40,960
        # llama3-gradient:70b   b5d6e9d0ae61    39 GB     36 seconds ago  context length      1,048,576   
 


def ignore_verbose_response(resp : str) -> str:
    try:
        resp = re.sub(r"\brule\b", "rule", resp, flags=re.IGNORECASE)
        resp = re.sub(r"\brule \b", "rule", resp, flags=re.IGNORECASE)
        resp = re.sub(r"(?i)\brule\s*\(", "rule(", resp)



        # pattern = r"rule\(.*?\)" # . = all characters , * repeats for all until it hits ), ? stops at the first ')'
        pattern = r"rule\s*\([^)]*\)"

        str_arr = re.findall(pattern, resp)
        str_builder = ""

        for rule in str_arr:
            str_builder +=f"{rule.strip()}\n"

        return str_builder
    except:
        print("error in verbose")
        return "error"
        



def local_api(gt_acl_file, gt_abac_rules_file, attribute_data_file, attribute_data_description_file, max_num_it, model, num_ctx):
    try:
        iterate_api_requests(gt_acl_file, gt_abac_rules_file, attribute_data_file, attribute_data_description_file, max_num_it, local_api_call, model, num_ctx)
        return
    except Exception as e:
            prepend_text_to_file("llm-research/session/cache/statistics.cache",f"Error in local_api.local_api: {e}\n")

            return
        


        #                        subprocess.run(['g++', '-std=c++20', '-o', os.path.join(folder_name, 'executable'), os.path.join(folder_name, program_file)])




def local_api_call(request_text, model, num_ctx):
    try:
        local_machine = False
        if not local_machine:
            print("Api Call")
            URL = "http://100.89.62.79:11434/api/generate"
            payload = {
                        "model": model,
                        "prompt": request_text,
                        "stream": False, 
                        "keep_alive" :"0s",
                        "options" :{"num_ctx":num_ctx},
        
                        
                        }
            r = requests.post(URL, json=payload, timeout=(10, 2000))
            r.raise_for_status()
            data = r.json()
            if "response" not in data:
                raise RuntimeError(f"ollama /api/generate missing 'response': {data}")
            response_message = data["response"].strip()
        else:
            client = Client(host="http://localhost:11434", timeout=32000)
            resp = client.chat(model=model, messages=[{"role":"user","content":request_text}])
            # resp is a dict in current client
            response_message = resp["message"]["content"].strip()

        
        print((response_message))
        print("=====================****************************************======================")

        final_output = re.sub(r"<think>.*?</think>\n?", "", response_message, flags=re.DOTALL).replace("\\", "")
        print(ignore_verbose_response(final_output))

        return final_output
    except Exception as e:
        prepend_text_to_file("llm-research/session/cache/statistics.cache",
                             f"Error in local_api.local_api_call: {e}\n")
        return ""


def main():

    request_text = "duplicate this for me 5 times every time change all the numbers from different numbers from 0-25 :rule( section one ; section 2 ; section 3; section 4) but change the numbers all to 0,  then tell me  a quick riddle"
    local_api_call(request_text, "qwen3:0.6b", 1000)

if __name__ == "__main__":
    main()

