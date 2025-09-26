##API CALL ON GEMINI-2.0-flash
import json
import requests
from helper_functions import read_entire_file, iterate_api_requests, prepend_text_to_file

def gemini_api(gt_acl_file, gt_abac_rules_file, attribute_data_file, attribute_data_description_file, max_num_it):

    iterate_api_requests(gt_acl_file, gt_abac_rules_file, attribute_data_file, attribute_data_description_file, max_num_it, gemini_api_call)
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


    payload_text = (
        payload.get("candidates", [{}])[0]
            .get("content", {})
            .get("parts", [{}])[0]
            .get("text", "")
    )

    cleaned_payload_text = payload_text.replace('`', "")
    return cleaned_payload_text

if __name__ == "__main__":
    # gemini_api_call()
    # print ("api call finalized")
    pass