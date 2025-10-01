import json
import requests
from openai import OpenAI
from ollama import Client
from anthropic import Anthropic
from helper_functions import * 
from mining import *

def openai_gpt5_api(gt_acl_file, gt_abac_rules_file, attribute_data_file, attribute_data_description_file, max_num_it, model, num_ctx):
    try:
        iterate_api_requests(gt_acl_file, gt_abac_rules_file, attribute_data_file, attribute_data_description_file, max_num_it, openai_gpt5_api_call, model, num_ctx)
        return
    except Exception as e:
        prepend_text_to_file("llm-research/session/cache/statistics.cache",f"Error in openai_gpt5_api.openai_gpt5_api_call: {e}\n")
        return "error"

def openai_gpt5_api_call(request_text):
    try:
        print(f"calling openai API...")

        client = OpenAI(
            # This is the default and can be omitted
            api_key="API_KEY",

            # 20 seconds (default is 10 minutes)
            timeout=800
        
        )
    
        response = client.responses.create(
            model="gpt-5",
            # instructions="You are a coding assistant that talks like a pirate.",
            input=request_text,
        )
        response_message= response.output_text

    
        return api_resp_cleaner(response_message)
    
    except Exception as e:
            prepend_text_to_file("llm-research/session/cache/statistics.cache",
                                f"Error in openai_gpt5_api.openai_gpt5_api_call: {e}\n")
            print(e)
            return ""
    
def anthropic_api(gt_acl_file, gt_abac_rules_file, attribute_data_file, attribute_data_description_file, max_num_it, model, num_ctx):
    try:
        iterate_api_requests(gt_acl_file, gt_abac_rules_file, attribute_data_file, attribute_data_description_file, max_num_it, anthropic_api_call, model, num_ctx)
        return
    except Exception as e:
            prepend_text_to_file("llm-research/session/cache/statistics.cache",f"Error in local_api.local_api: {e}\n")

            return
        
def anthropic_api_call(request_text ):
     
        try:
            client = Anthropic()
            client = Anthropic(api_key = "")

            response = client.beta.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1024,
                messages=[
                    {"role": "user", "content":request_text}
                ],
                betas=["context-1m-2025-08-07"]
            )

            response_message= response.content[0].text

            return api_resp_cleaner(response_message)

            # return final_output
        except Exception as e:
            prepend_text_to_file("llm-research/session/cache/statistics.cache",
                                f"Error in anthropic_api.anthropic_api_call: {e}\n")
            print(e)
            return ""

def gemini_api(gt_acl_file, gt_abac_rules_file, attribute_data_file, attribute_data_description_file, max_num_it, model, num_ctx):

    iterate_api_requests(gt_acl_file, gt_abac_rules_file, attribute_data_file, attribute_data_description_file, max_num_it, gemini_api_call, model, num_ctx)
    return
   
def gemini_api_call(request_text):

    key_file ="keys/geminiKey.txt"
    
    print("CALLLING GEMINI API..")

    try:
        gemini_key = read_entire_file(key_file)

    except FileNotFoundError as e:
        prepend_text_to_file("llm-research/session/cache/statistics.cache",f"Error reading file: {e}\n")
        return
    except Exception as e:
        prepend_text_to_file("llm-research/session/cache/statistics.cache",f"Unexpected read error: {e}\n")
        return
    

    # send to Gemini 
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    headers = {"Content-Type": "application/json", "X-goog-api-key": gemini_key}
    data = {
        "contents": [
            {
                "parts": [
                    {"text": request_text}
                ]
            }
        ]
    }

    try:
        resp = requests.post(url, headers=headers, json=data)
        resp.raise_for_status()
    except requests.exceptions.Timeout:
        prepend_text_to_file("llm-research/session/cache/statistics.cache", f"HTTP error: request timed out\n")
        return
    except requests.exceptions.RequestException as e:
        prepend_text_to_file("llm-research/session/cache/statistics.cache",f"HTTP error: {e}\n")

        return

    try:
        payload = resp.json()
    except json.JSONDecodeError:
        prepend_text_to_file("llm-research/session/cache/statistics.cache",f"Response was not valid JSON.\n")

        
        return


    response_message = (
        payload.get("candidates", [{}])[0]
            .get("content", {})
            .get("parts", [{}])[0]
            .get("text", "")
    )

    return api_resp_cleaner(response_message)

def local_api(gt_acl_file, gt_abac_rules_file, attribute_data_file, attribute_data_description_file, max_num_it, model, num_ctx):
    try:
        iterate_api_requests(gt_acl_file, gt_abac_rules_file, attribute_data_file, attribute_data_description_file, max_num_it, local_api_call, model, num_ctx)
        return
    except Exception as e:
            prepend_text_to_file("llm-research/session/cache/statistics.cache",f"Error in local_api.local_api: {e}\n")

            return
        
def local_api_call(request_text, model, num_ctx):
    #READ ME:

    #LLMs available through our server (smaller LLMs do not have a context window large enough to reason)
        # reflection:70b        5084e77c1e10    39 GB     45 hours ago    context length      131,072 # solid
        # llama3.3:70b          a6eb4748fd29    42 GB     46 hours ago    context length      131,072 #long time outs needed to test , still need to see format
        # qwen:72b              e1c64582de5c    41 GB     2 days ago      context length      32,768  # do not use, responds with blanks or gibberish.if ran save till the end
        # gemma3:27b            a418f5838eaf    17 GB     3 days ago      context length      131,072 # solid
        # phi4-reasoning:14b    47e2630ccbcd    11 GB     3 days ago      context length      40,000  # small but good
        # gpt-oss:120b          f7f8e2f8f4e0    65 GB     2 weeks ago     context length      131,072 #best local option
        # deepseek-r1:70b       d37b54d01a76    42 GB     2 weeks ago     context length      131,072  # should rn
        # gpt-oss:latest        aa4295ac10c3    13 GB     2 weeks ago     context length      131,072  #redundant
        # llama3.1:70b          711a9e8463af    42 GB     3 weeks ago     context length      131,072 #use llama 3.3
        # qwen3:32b             030ee887880f    20 GB     3 weeks ago     context length      40,960  #low priority 
        # gpt-oss:20b           aa4295ac10c3    13 GB     3 weeks ago     context length      131,072 #worthy of testing
        # qwen3:0.6b            7df6b6e09427    522 MB    3 weeks ago     context length      40,960 #way too small to waste time on it 
        # llama3-gradient:70b   b5d6e9d0ae61    39 GB     36 seconds ago  context length      1,048,576   #run but run last, with same or a bit more of a window than openai

    local = True ##Toggle True if runnign on secLab Mac

    print(f"model : {model}, num_ctx : {num_ctx}")
    try:
        host = "http://localhost:11434" if local else "http://100.89.62.79:11434" ##need to be on white list to reach API
        print(f"host : {host}")
        client = Client(host=host, timeout=2000)

        resp = client.chat(
            model=model,
            messages=[{"role": "user", "content": request_text}],
            keep_alive=1200,
            options={"num_ctx": num_ctx},
        )

        response_message = resp["message"]["content"].strip()

        return api_resp_cleaner(response_message)
    
    except Exception as e:
        prepend_text_to_file("llm-research/session/cache/statistics.cache",
                             f"Error in local_api.local_api_call: {e}\n")
        return ""
        
def manual_api(gt_acl_file, gt_abac_rules_file, attribute_data_file, attribute_data_description_file, max_num_it, model, num_ctx):
    #NOTE: We clear all data from GPT or manual models before running them.
    #   this is to simulate a API call that would not retain previous chats in memory 
    iterate_api_requests(gt_acl_file, gt_abac_rules_file, attribute_data_file, attribute_data_description_file, max_num_it, manual_api_call, model, num_ctx)
    return

def manual_api_call(request_text):
    
    print(f"Copy text from: prompts/complete-prompt.txt\n Every iteration WILL have a unique prompt\n")
    input_confirm = input (f"Paste in response to the manual-input.txt and type 'd' when done\n>>$")

    if input_confirm !='d': 
        print(f"ERROR: input rules and try again\n")
        return    
    

    strip_backslashes_from_file("ignore/manual-input.txt")
    response_message = file_to_text("ignore/manual-input.txt")
    
    return api_resp_cleaner(response_message)
