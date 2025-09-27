import os
from openai import OpenAI
from helper_functions import iterate_api_requests
from helper_functions import prepend_text_to_file, iterate_api_requests



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

            api_key="nope",
            # 20 seconds (default is 10 minutes)
            timeout=20.0
        
        )
        response = client.responses.create(
            model="gpt-5",
            # instructions="You are a coding assistant that talks like a pirate.",
            input=request_text,
        )

        return(response.output_text)

    except Exception as e:
            print() 
            prepend_text_to_file("llm-research/session/cache/statistics.cache",f"Error in openai_gpt5_api.openai_gpt5_api_call: {e}\n")
            return "error"


