import ollama
import requests
import json

# from helper_functions import read_entire_file, clear_file, prompt_generator, append_to_file
#MAKE SURE SSH TUNNEL IS SET UP TO SECLAB@IP!!!!!!
#IF NOT RUNNING ON SEC LAB MAC 
#TODO find and link youtube video that showed me this fucntion


def local_api_call():
   
        # complete_request = "Give me a quick bio on Aubry 'Drake' Graham"

        # client = ollama.Client()
        # Available models:
        # NAME SIZE
        # 11ama3.1:70b  - 42 GB
        # qwen3:32b     - 20 GB
        # gpt-oss:20b   - 13 GB
        # qwens:0.6b    - 522 MB  #RUNNING

    
        # print("local api request sent...")
        # response  = client.generate(model=model, prompt=complete_request)

        # print("QWEN RESPONSE:")

        # print(response.response)
        # return
    model = "qwen3:0.6b"
    prompt = "write me a hello program that asks for a name and prints hello + name, write it in python"
    URL = "http://100.89.62.79:11434/api/generate"

    payload = {
        "model": model,
        "prompt": prompt,
        # optional:
        # "stream": True,  # default True
        # "options": {"temperature": 0.2}
    }

    print("making request")
    with requests.post(URL, json=payload, stream=False, timeout=30) as r:
        r.raise_for_status()
        for line in r.iter_lines(decode_unicode=True):
            if not line:
                continue
            msg = json.loads(line)
            if "response" in msg:
                print(msg["response"], end="")
            if msg.get("done"):
                break
    print("------------")
    print(json)

    return



def main():
    local_api_call()

if __name__ == "__main__":
    main()

