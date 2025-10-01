import os, re
import shutil

def write_map_to_file(path: str, data_map: dict):
    with open(path, "w", encoding="utf-8") as f:
        for key, value in data_map.items():
            f.write(f"{key} : {value}\n")

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

#AI generated code
def clear_text_files(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith((".txt", ".cache")):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, "w", encoding="utf-8"):
                pass

    return

def ensure_rule_file(path: str):
    
    # Check for existing rules
    has_rule = False
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip().startswith("rule"):
                has_rule = True
                break

    # if no rule, append a placeholder
    if not has_rule:
        with open(path, "a", encoding="utf-8") as f:
            f.write("rule (<NOT>; <LLM>; <GENERATED>; <RULE>)\n")

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

def strip_backslashes_from_file(filepath: str) -> None:
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    cleaned = content.replace("\\", "")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(cleaned)


def move_and_rename_all(src_dir, dest_dir, name_prefix, timestamp):
    try:
        # one consistent timestamp for everything

        # Rename the parent folder itself
        folder_name = os.path.basename(src_dir.rstrip(os.sep))
        new_folder_name = f"{name_prefix}_{timestamp}_{folder_name}"
        new_folder_path = os.path.join(dest_dir, new_folder_name)

        # Copy the whole directory first
        shutil.copytree(src_dir, new_folder_path)

        # Walk through everything we just copied and rename items
        for root, dirs, files in os.walk(new_folder_path, topdown=False):
            # Rename files
            for fname in files:
                old_path = os.path.join(root, fname)
                new_name = f"{name_prefix}_{timestamp}_{fname}"
                new_path = os.path.join(root, new_name)
                os.rename(old_path, new_path)

            # Rename directories
            for dname in dirs:
                old_path = os.path.join(root, dname)
                new_name = f"{name_prefix}_{timestamp}_{dname}"
                new_path = os.path.join(root, new_name)
                os.rename(old_path, new_path)

        return new_folder_path

    except Exception as e:
        print(f"Error in file_manip.move_and_rename_all: {e}")
        return

##FROM ACL TOOLS

def file_to_set(file_name):
    
    lines =  set()
    with open (file_name, "r", encoding="utf-8") as f:
        for line in f:
            lines.add(line.strip())
    return lines

def prepend_text_to_file(filename, text):
    with open(filename, "r", encoding="utf-8") as f:
        original_content = f.read()
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)
        f.write(original_content)

    return

def load_rules_from_file(path: str):
    rules = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("rule"):
                rules.append(line)
    return rules

def file_to_text(filename):
    temp_string = ""

    with open (filename, "r", encoding="utf-8") as f:
        temp_string += f.read().strip()
    
    return temp_string

def append_to_file(filename, text):
    with open(filename, "a", encoding="utf-8") as f:
        f.write(str(text))

    return

def count_lines(path: str) -> int:
    count = 0
    with open(path, "r", encoding="utf-8") as f:
        for _ in f:
            count += 1
    return count

##FROM rule_syntax_analyzer

def printArr(arr):
    for x in arr:
        print(x)

def prepend_text_to_file(filename, text):
    with open(filename, "r", encoding="utf-8") as f:
        original_content = f.read()
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)
        f.write(original_content)

    return


##FROM llm_main for config parsing
def config_parser(file : str):
# to run anthropic you need to be in a vm, no clue why but i could only install the packages with tha
    execution_count = None
    max_num_it = None
    api_arr = []
    org_arr = []

 
    with open(file, "r", encoding="utf-8") as f:
        for line in f:
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue

            if stripped.startswith("execution"):
                execution_count = int(stripped.split(">")[1].strip())

            elif stripped.startswith("iteration"):
                max_num_it = int(stripped.split(">")[1].strip())

            elif stripped.startswith("api"):
                api_arr.append(stripped.split(">")[1].strip())

            elif stripped.startswith("org"):
                org_arr.append(stripped.split(">")[1].strip())


    return execution_count, max_num_it, api_arr, org_arr

def org_parser(org_line: str):
    # Expect format: "org > name(file1; file2; file3; file4)"
    org_name, rest = org_line.split("(", 1)
    org_name = org_name.replace("org >", "").strip()

    parts = rest.rstrip(")").split(";")
    parts = [p.strip() for p in parts]

         # org,          gt_acl_file,   gt_abac_rules_file, attribute_data_description_file,    attribute_data_file
    return org_name,     parts[0],      parts[1],           parts[2],                           parts[3]

##api_calls.py

def api_resp_cleaner(response_message):

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