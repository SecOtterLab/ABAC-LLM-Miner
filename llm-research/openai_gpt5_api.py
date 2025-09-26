import os
from openai import OpenAI
from helper_functions import iterate_api_requests
from helper_functions import read_entire_file, iterate_api_requests



def openai_gpt5_api(gt_acl_file, gt_abac_rules_file, attribute_data_file, attribute_data_description_file, max_num_it):

    iterate_api_requests(gt_acl_file, gt_abac_rules_file, attribute_data_file, attribute_data_description_file, max_num_it, openai_gpt5_api_call)
    return





def openai_gpt5_api_call(request_text):

    print(f"calling openai API...")

    client = OpenAI(
        # This is the default and can be omitted

        # 20 seconds (default is 10 minutes)
        timeout=20.0
    
    )
    response = client.responses.create(
        model="gpt-5",
        # instructions="You are a coding assistant that talks like a pirate.",
        input=request_text,
    )

    return(response.output_text)


