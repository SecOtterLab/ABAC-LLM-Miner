# import ollama
import requests
import re
from helper_functions import iterate_api_requests

#READ ME:
    # To run one must be hosting the right LLM on ollama 
    # our url is not avialble to users with an ip not in our white list
    # LLMs with a context window large enough and available to us are the following:
        # deepseek-r1:70b       d37b54d01a76    42 GB     
        # gpt-oss:120b          f7f8e2f8f4e0    65 GB      
        # llama3.1:70b          711a9e8463af    42 GB     
        # llama3.3:70b          a6eb4748fd29    42 GB
        # qwen:72b              e1c64582de5c    41 GB 
        # reflection:70b        5084e77c1e10    39 GB   

    #LLMs available through our server (smaller LLMs do not have a context window large enough to reason)
        # gemma3:27b            a418f5838eaf    17 GB     26 hours ago    
        # magistral:24b         27bcbbf6d324    14 GB     26 hours ago    
        # phi4-reasoning:14b    47e2630ccbcd    11 GB     26 hours ago    
        # gpt-oss:latest        aa4295ac10c3    13 GB     13 days ago     
        # qwen3:32b             030ee887880f    20 GB     3 weeks ago     
        # gpt-oss:20b           aa4295ac10c3    13 GB     3 weeks ago     
        # qwen3:0.6b            7df6b6e09427    522 MB    3 weeks ago     
    

def local_api(gt_acl_file, gt_abac_rules_file, attribute_data_file, attribute_data_description_file, max_num_it):

    iterate_api_requests(gt_acl_file, gt_abac_rules_file, attribute_data_file, attribute_data_description_file, max_num_it, local_api_call)
    return



def local_api_call(request_text):
    
    model = "phi4-reasoning:14b"
    # prompt = "what is 5 to the 3rd power"
    URL = "http://100.89.62.79:11434/api/generate"

    payload = {
        "model": model,
        "prompt": request_text,
        "stream": False  # still streams, but we capture
        # "format" : "json" ollam does not respond with consistent json, too unpredicatble auto response is more predicatble with <think></think> tags
    }

    r = requests.post(URL, json=payload, timeout=(10, 6000)) #10 = TCP connection 420 is timeout 
    r.raise_for_status()

    response_message = r.json()["response"].strip()
    final_output = re.sub(r"<think>.*?</think>\n?", "", response_message, flags=re.DOTALL)
    print(final_output)
    return final_output



# def main():
#     local_api_call()

# if __name__ == "__main__":
#     main()

