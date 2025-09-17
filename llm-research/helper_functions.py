#Functions to assist in the llm-research folder .py files
#includes but is not limmited to files to open text files
# combine text files
import os, sys
from acl_tools import compare_acl, generate_acl
from myabac import parse_abac_file


def write_to_file(filename, lines):

    with open(filename, "w", encoding="utf-8") as f:
        for line in lines:
            f.write(line +"\n")
    
    return

def clear_file(filename):
    with open(filename,"w", encoding="utf-8"):
        pass

    return

def read_entire_file(filename):
    
    with open (filename, "r", encoding="utf-8") as f:
        return f.read().strip()
    
    return

def file_to_text(filename):
    temp_string = ""

    with open (filename, "r", encoding="utf-8") as f:
        temp_string += f.read().strip()
    
    return temp_string

#removed all calls, I just copied the data set and removed the rules.
def read_until_marker(filename, stop_marker):
    lines = []
    with open (filename, "r", encoding="utf-8" ) as f:
        for line in f:
            if line.strip() == stop_marker:
                break
            lines.append(line.rstrip())
        return "\n".join(lines).strip()

def append_to_file(filename, text):
    with open(filename, "a", encoding="utf-8") as f:
        f.write(str(text))

    return

def write_text_to_file(filename, text):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(str(text) + "\n")

    return

def prepend_text_to_file(filename, text):
    with open(filename, "r", encoding="utf-8") as f:
        original_content = f.read()
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)
        f.write(original_content)

    return
    
def append_from_file(dest_file, src_file):
    with open(src_file, "r", encoding="utf-8") as src:
        content = src.read()
    with open(dest_file, "a", encoding="utf-8") as dst:
        dst.write(content)

    return

def prepend_file(dest_file, src_file):
    with open(src_file, "r", encoding="utf-8") as src:
        prepend_content = src.read()
    with open(dest_file, "r", encoding="utf-8") as dst:
        original_content = dst.read()
    with open(dest_file, "w", encoding="utf-8") as dst:
        dst.write(prepend_content)  
        dst.write(original_content)  

    return

def prompt_generator(gt_acl_file, attribute_data_file, attribute_data_description_file, prompt_file, complete_request_file , comparison_file ):
   
    clear_file(complete_request_file)
    
    #if comparison is not empty include it
    comparison = read_entire_file(comparison_file)
    include_comparison = bool(comparison.strip())

    # build a single request file
    sections = {
        "LLM REQUEST": prompt_file,
        "## ATTRIBUTE_DESCRIPTION ##": attribute_data_description_file,
        "## ATTRIBUTE_DATA ##": attribute_data_file,
        "## GROUND_TRUTH_ACL ##":gt_acl_file
        }

    if include_comparison:
        sections["## ACL_COMPARISON ##"]= comparison_file
        sections["## CURRENT_RULES ##"]= "llm-research/session/session-llm-response.txt"
    else:
        pass 

    with open(prompt_file, "r", encoding="utf-8") as f:
        for line in f:
            marker = line.strip()
            if marker in sections:
                append_to_file(complete_request_file, line)
                append_from_file(complete_request_file, sections[marker])
            else:
                append_to_file(complete_request_file, line)
            
    return



#AI generated code
def clear_text_files(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith((".txt", ".cache")):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, "w", encoding="utf-8"):
                pass

    return



def iterate_api_requests(gt_acl_file, attribute_data_file, attribute_data_description_file,  api_call, max_num_it):
    # generated file #: declare the location on the complete request being made
    # this file should contain everyhting we are feeding the LLM to make the rules.
    complete_request_file = "prompts/complete-prompt.txt"
    prompt_file = "prompts/initial-starting-prompt.txt"
    comparison_file ="prompts/empty.txt"

    prompt_generator(gt_acl_file, attribute_data_file, attribute_data_description_file, prompt_file, complete_request_file , comparison_file )
    
    append_from_file("llm-research/session/output/complete-initial-prompt.txt", complete_request_file )
    print("ITERATING API CALLS..")

    #TODO: delcare output stats files and write to them
    

    is_match = False
    counter = 0
    session_abac_file ="llm-research/session/session-abac.txt"
    session_acl_file="llm-research/session/session-ACL.txt"
    session_comparison_file="llm-research/session/session-comparison.txt"
    session_llm_response_file="llm-research/session/session-llm-response.txt"

    #The initial complete prompt file, to make the initial request

    complete_request = read_entire_file(complete_request_file)

    # The api_call function will return text of the response.
    payload_text = api_call(complete_request)

    #output the abac rules to a file for testing
    if(payload_text is None):
        print(f"skipping iteration: payload not received\n")
        sys.exit()
    else:
        with open(session_llm_response_file, "w", encoding="utf-8") as of:
            of.write(payload_text)
    
    is_match = create_session_data(session_abac_file, attribute_data_file, session_llm_response_file, session_acl_file, gt_acl_file, session_comparison_file)
    write_to_logs(counter)

    counter +=1

    while(is_match is False and counter < max_num_it):

        print("api loop running")

        prompt_file = ("prompts/subsequent-starting-prompt.txt")
        prompt_generator(gt_acl_file, attribute_data_file, attribute_data_description_file,prompt_file, complete_request_file , session_comparison_file )

        complete_request = read_entire_file(complete_request_file)

        # The api_call function will return text of the response.
        payload_text = api_call(complete_request)
        
        #output the abac rules to a file for testing
        if(payload_text is None):
            print(f"skipping iteration: payload not received\n")
            counter +=1
            continue
        else:
            with open(session_llm_response_file, "w", encoding="utf-8") as of:
                of.write(payload_text)

        is_match = create_session_data(session_abac_file, attribute_data_file, session_llm_response_file, session_acl_file, gt_acl_file, session_comparison_file)
        write_to_logs(counter)

        counter +=1

    return


def create_session_data(session_abac_file, attribute_data_file, session_response, llm_acl_file, gt_acl_file, session_comparison_file):
        #clear the file for the iteration
        clear_file(session_abac_file)
        # write the abac policy (llm version that has no rules) into the session abac file
        append_from_file(session_abac_file, attribute_data_file)

        # write the rules (generated by the LLM) into the session abac file
        append_from_file(session_abac_file, session_response)

        # create abac data structures from the session abac file (the one generated with LLM abac rules)
        user2, res2, rule2 = parse_abac_file(session_abac_file)

        # make a new ACL using the rules given by the LLM
        generate_acl(user2, res2, rule2, llm_acl_file)

        #store the comparison in a text object
        temp_text, is_match = compare_acl(gt_acl_file,llm_acl_file)

        #write the comparison to a text file
        write_to_file(session_comparison_file, temp_text)

        return is_match

def write_to_logs(num_it):

    divider_text = (f"\n===============================================================\nITERATION : {num_it}\n===============================================================\n")
    
    prepend_file("llm-research/session/cache/complete-prompt.cache", "prompts/complete-prompt.txt")
    prepend_text_to_file("llm-research/session/cache/complete-prompt.cache", divider_text)

    prepend_file("llm-research/session/cache/session-abac.cache", "llm-research/session/session-abac.txt")
    prepend_text_to_file("llm-research/session/cache/session-abac.cache", divider_text)

    prepend_file("llm-research/session/cache/session-ACL.cache", "llm-research/session/session-ACL.txt")
    prepend_text_to_file("llm-research/session/cache/session-ACL.cache", divider_text)

    prepend_file("llm-research/session/cache/session-comparison.cache", "llm-research/session/session-comparison.txt")
    prepend_text_to_file("llm-research/session/cache/session-comparison.cache", divider_text)

    prepend_file("llm-research/session/cache/session-llm-response.cache", "llm-research/session/session-llm-response.txt")
    prepend_text_to_file("llm-research/session/cache/session-llm-response.cache", divider_text)
    #write to output file too
    prepend_file("llm-research/session/output/generated-rules.txt", "llm-research/session/session-llm-response.txt")
    prepend_text_to_file("llm-research/session/output/generated-rules.txt", divider_text)


    return
