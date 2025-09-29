##API CALL ON GEMINI-2.0-flash
import json
import requests
import re
from helper_functions import read_entire_file, iterate_api_requests, prepend_text_to_file, append_to_file


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

    final_output = response_message.replace('`', "")
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

if __name__ == "__main__":
    # gemini_api_call()
    # print ("api call finalized")
    pass