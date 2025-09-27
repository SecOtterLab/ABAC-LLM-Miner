# import ollama
import requests
import re
from helper_functions import iterate_api_requests, prepend_text_to_file
import sys
from ollama import chat
from ollama import ChatResponse
from ollama import Client

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
        # llama3-gradient:8b downloading max context length  1,000,000 
    

def local_api(gt_acl_file, gt_abac_rules_file, attribute_data_file, attribute_data_description_file, max_num_it):
    try:
        iterate_api_requests(gt_acl_file, gt_abac_rules_file, attribute_data_file, attribute_data_description_file, max_num_it, local_api_call)
        return
    except Exception as e:
            prepend_text_to_file("llm-research/session/cache/statistics.cache",f"Error in local_api.local_api: {e}\n")

            return
        



def local_api_call(request_text):
    try:
        #switch when running on mac studio
        local_machine  = False
        # model = "phi4-reasoning:14b"   

        if not local_machine:
            URL = "http://100.89.62.79:11434/api/generate"

            payload = {
                "model": model,
                "prompt": request_text,
                "stream": False  # still streams, but we capture
                # "format" : "json" ollam does not respond with consistent json, too unpredicatble auto response is more predicatble with <think></think> tags
            }

            r = requests.post(URL, json=payload, timeout=(10, 2000)) #10 = TCP connection 420 is timeout 
            r.raise_for_status()

            response_message = r.json()["response"].strip()
            final_output = re.sub(r"<think>.*?</think>\n?", "", response_message, flags=re.DOTALL)
            final_output = final_output.replace("\\", "")
            print(final_output)
            return final_output
        
        else: 
            client = Client(host='http://localhost:11434', timeout=32000)  # seconds
            resp = client.chat(model=model, messages=[{'role':'user','content':request_text}])
            # print(resp)

            response_message = resp['message']['content'].strip()
            final_output = re.sub(r"<think>.*?</think>\n?", "", response_message, flags=re.DOTALL)
            final_output = final_output.replace("\\", "")
            print(final_output)
            return final_output
    
    except Exception as e:
            prepend_text_to_file("llm-research/session/cache/statistics.cache",f"Error in local_api.local_api_call: {e}\n")
            return


def main():
    request_text = "what is 5 to the 3rd power, answer only"
    local_api_call(request_text)

if __name__ == "__main__":
    main()

