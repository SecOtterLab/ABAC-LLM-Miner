import requests, json
from helper_functions import iterate_api_requests, prepend_text_to_file, append_to_file
import re
from anthropic import Anthropic
import time

#claud price per token : https://docs.claude.com/en/docs/about-claude/pricing
# context window 200K https://www.anthropic.com/claude/opus
def ignore_verbose_response(resp : str) -> str:
    try:
        resp = re.sub(r"\brule\b", "rule", resp, flags=re.IGNORECASE)
        resp = re.sub(r"\brule \b", "rule", resp, flags=re.IGNORECASE)
        resp = re.sub(r"(?i)\brule\s*\(", "rule(", resp)

        pattern = r"rule\s*\([^)]*\)"

        str_arr = re.findall(pattern, resp)
        str_builder = ""

        for rule in str_arr:
            str_builder +=f"{rule.strip()}\n"

        return str_builder
    except:
        print("error in verbose")
        return "error"
        




def anthropic_api(gt_acl_file, gt_abac_rules_file, attribute_data_file, attribute_data_description_file, max_num_it, model, num_ctx):
    try:
        iterate_api_requests(gt_acl_file, gt_abac_rules_file, attribute_data_file, attribute_data_description_file, max_num_it, anthropic_api_call, model, num_ctx)
        return
    except Exception as e:
            prepend_text_to_file("llm-research/session/cache/statistics.cache",f"Error in local_api.local_api: {e}\n")

            return
        



def anthropic_api_call(request_text ):
     
        try:
            # model="claude-sonnet-4-20250514"
            # # model="claude-opus-4-1-20250805"
             
            # api_key = "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"
            # url = "https://api.anthropic.com/v1/messages"

            # headers = {
            #     "x-api-key": api_key,
            #     "anthropic-version": "2023-06-01",
            #     "content-type": "application/json",
            # }

            # data = {
            #     "model": model,
            #     "max_tokens": 32000, #max token output that anthropic will let you call for opus 4-1
            #     "messages": [{"role": "user", "content": request_text}],
            #     # "betas" : ["context-1m-2025-08-07"],
            # }

            # resp = requests.post(url, headers=headers, data=json.dumps(data))

            # j = resp.json()

            # print(j["content"][0]["text"])
            # response_message= j["content"][0]["text"]


            client = Anthropic()
<<<<<<< HEAD
            client = Anthropic(api_key = "")
=======
            client = Anthropic(api_key = "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")
>>>>>>> cef652b8d82178aca5750fe1da64ccbfe6dfe54e

            response = client.beta.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1024,
                messages=[
                    {"role": "user", "content":request_text}
                ],
                betas=["context-1m-2025-08-07"]
            )

            
            response_message= response.content[0].text
            # print(response_message)
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
            return(response_message)

            # return final_output
        except Exception as e:
            prepend_text_to_file("llm-research/session/cache/statistics.cache",
                                f"Error in anthropic_api.anthropic_api_call: {e}\n")
            print(e)
            return ""


def main():

    request_text = "return this same next line to me replace the numbers and make 3 of them and return all 3: this is the line  rule(1 ; 2; 3; 4)"
    print(anthropic_api_call(request_text))

if __name__ == "__main__":
    main()

