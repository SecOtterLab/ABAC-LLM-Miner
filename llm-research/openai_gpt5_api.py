import re
from openai import OpenAI
from helper_functions import prepend_text_to_file, iterate_api_requests, append_to_file

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
            api_key="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",

            # 20 seconds (default is 10 minutes)
            timeout=800
        
        )
    
        response = client.responses.create(
            model="gpt-5",
            # instructions="You are a coding assistant that talks like a pirate.",
            input=request_text,
        )
        response_message= response.output_text

        print("payload recieved ")
        # print((response_message))
        form_str = f"\n=====================*****************RAW***********************====================================\n"
        append_to_file("llm-research/session/cache/raw-response.cache", str(form_str))
        append_to_file("llm-research/session/cache/raw-response.cache", str(response_message))
        form_str = (f"\n=====================*****************MINOR FORMATTING***********************======================\n")
        append_to_file("llm-research/session/cache/raw-response.cache", str(form_str))

        final_output = re.sub(r"<think>.*?</think>\n?", "", response_message, flags=re.DOTALL).replace("\\", "")
        final_output = (ignore_verbose_response(final_output))
        append_to_file("llm-research/session/cache/raw-response.cache", str(final_output))
        form_str = (f"\n=====================*****************END***********************==================================\n")
        append_to_file("llm-research/session/cache/raw-response.cache", str(form_str))





        return final_output
    
    except Exception as e:
            prepend_text_to_file("llm-research/session/cache/statistics.cache",
                                f"Error in openai_gpt5_api.openai_gpt5_api_call: {e}\n")
            print(e)
            return ""
    
