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

def unwrap_rule(str) -> str:
    try:
        str = str.strip()
        str = str.replace("rule", "",1)
        str = str.replace("(", "")
        str = str.replace(")", "")
        return str
    except Exception as e:
        prepend_text_to_file("llm-research/session/cache/statistics.cache",f"Error in rule_syntax_analyzer.unwrap_rule: {e}\n")
        return "error"

def split_rule(str):

    try:
        #split the string and convert to arr at ';'
        atomic_arr = [s.strip() for s in str.split(";")]

        if len(atomic_arr) < 4:
            atomic_arr += [""] * (4 - len(atomic_arr))
        
        #if there are empty ones we note them as empty
        # helps with debugging and will prevent breaking incase llm rules are poor
        if not atomic_arr[0] or not atomic_arr[0].strip():
            atomic_arr[0] = "<emptySubCond>"

        if not atomic_arr[1] or not atomic_arr[1].strip():
            atomic_arr[1] = "<emptyResCond>"

        if not atomic_arr[2] or not atomic_arr[2].strip():
            atomic_arr[2] = "<emptyActs>"

        if not atomic_arr[3] or not atomic_arr[3].strip():
            atomic_arr[3] = "<emptyCons>"

        return atomic_arr
    
    except Exception as e:
        prepend_text_to_file("llm-research/session/cache/statistics.cache",f"Error in rule_syntax_analyzer.split_rule: {e}\n")


        return []

def printArr(arr):
    for x in arr:
        print(x)

import re

def sort_sets_in_line(text: str) -> str:
    pattern = re.compile(r"\{([^}]*)\}")

    try:

        def sort_one(m: re.Match) -> str:
            # split on commas and/or whitespace, drop empties
            items = [t for t in re.split(r"[,\s]+", m.group(1).strip()) if t]
            items.sort(key=str.casefold)  # case-insensitive, preserve original
            return "{" + "*".join(items) + "}"  # use * as the separator

        return pattern.sub(sort_one, text)
    
    except Exception as e:
        prepend_text_to_file("llm-research/session/cache/statistics.cache",f"Error in rule_syntax_analyzer.sort_sets_in_line: {e}\n")
        return "error"



#breaks down a set of rules into a data structure
# allows us to break down all the rules down once instead of every time we need to compare them
def rule_to_data_set(arr, arr_name):
    try: 
        temp_arr = []
        for i in range ( len(arr)):
            unaltered_rule = arr[i]
            arr[i] = sort_sets_in_line(arr[i])
            arr[i] = unwrap_rule(arr[i])
            section_arr = split_rule(arr[i])
            id = f"{arr_name} {i}"
            temp_arr.append({"id": id, "subCond": section_arr[0] , "resCond": section_arr[1], "acts":str(section_arr[2]) , "cons":section_arr[3], "rule": unaltered_rule})

        return temp_arr
    
    except Exception as e:
        prepend_text_to_file("llm-research/session/cache/statistics.cache",f"Error in rule_syntax_analyzer.rule_to_data_set: {e}\n")


        return []

def atomic_section(str):
    try:
        # print(str)
        atomic_arr = [s.strip() for s in str.split(",")]
        #remove sets of brackets for easier parsing
        # for i in range (len(atomic_arr)):
        #     atomic_arr[i] = atomic_arr[i].replace("{", "").replace("}", "")

        atomic_arr.sort()
        # print(f"=============AAS====================\n")

        # printArr(atomic_arr)
        # print(f"=================================\n")
        return atomic_arr
    
    except Exception as e:
        prepend_text_to_file("llm-research/session/cache/statistics.cache",f"Error in rule_syntax_analyzer.atomic_section: {e}\n")


        return []
    
    

def sub_atomic_section(str):

    try:
        atomic_arr = [s.strip() for s in str.split(" ")]
        return atomic_arr
    
    except Exception as e:
        prepend_text_to_file("llm-research/session/cache/statistics.cache",f"Error in rule_syntax_analyzer.sub_atomic_section: {e}\n")
        return []
    

def str_set_to_arr(str):

    try:
        #take a string of set {r w x} and return an arr [r, w, x]
        atomic_arr = [s.strip().replace("{", "").replace("}","") for s in str.split("*")]
        return atomic_arr
    
    except Exception as e:
        prepend_text_to_file("llm-research/session/cache/statistics.cache",f"Error in rule_syntax_analyzer.str_set_to_arr: {e}\n")
        return []

    
def jaccard(str1, str2):
    #arguements are string

    set1 = set(str_set_to_arr(str1))
    set2 = set(str_set_to_arr(str2))

    intersection = len(set1 & set2)
    union = len(set1 | set2)

    if union == 0:
        return 0

    # jacc_value = float(intersection / union)

    return float(intersection / union)


def rule_set_syntax_analyzer(rules1, rules2):

    try: 
        # accept paths or lists
        if isinstance(rules1, str):
            rules1 = load_rules_from_file(rules1)
        if isinstance(rules2, str):
            rules2 = load_rules_from_file(rules2)

        arr1 = rule_to_data_set(rules1, "GT")
        arr2 = rule_to_data_set(rules2, "LLM") 
        jacc_total = 0
        best_match ={}


        for rule1 in arr1:
            # print(gt_rule)
            best_match[rule1['rule']] =("EMPTY_BY_DEFAULT", 0)

            for rule2 in arr2:
                # print(llm_rule)
                sum_value = 0
                
                sum_value += analyze_atomic(rule1["subCond"], rule2["subCond"])
                sum_value += analyze_atomic(rule1["resCond"], rule2["resCond"])
                sum_value += jaccard(rule1["acts"], rule2["acts"])
                sum_value += analyze_atomic(rule1["cons"], rule2["cons"])

                # print(f"==============Analysis===========================================================================================\n")
                # print(f"subCond: {rule1["subCond"]} || {rule2["subCond"]}  == {analyze_atomic(rule1["subCond"], rule2["subCond"])}\n")
                # print(f"resCond: {rule1["resCond"]} || {rule2["resCond"]}  ==     {analyze_atomic(rule1["resCond"], rule2["resCond"])}\n")
                # print(f"acts: {rule1["acts"]} || {rule2["acts"]}  == {jaccard(rule1["acts"], rule2["acts"])}\n")
                # print(f"cons: {rule1["cons"]} || {rule2["cons"]}  == { analyze_atomic(rule1["cons"], rule2["cons"])}\n")
                # print(f"{rule1["rule"]} || {rule2["rule"]} || Score: {sum_value/4}")


                avg_value = (sum_value/4)

                if avg_value > best_match[rule1['rule']][1]:
                    best_match[rule1['rule']] = (rule2["rule"], avg_value)


        for key, value in best_match.items():
            # print(f"{key} => {value}\n")
            jacc_total += value[1]


        if len(best_match) == 0:
            return 0, {}
        
        jacc_avg = jacc_total/len(best_match)
        
        # print(f"TOTAL JACC  AVG: {jacc_avg}")

        return jacc_avg, best_match
    
    except Exception as e:
        prepend_text_to_file("llm-research/session/cache/statistics.cache",f"Error in rule_syntax_analyzer.rule_set_syntax_analyzer: {e}\n")
        return 0, {}


def populate_empty_tag(arr, amount):
    try: 
        for _ in range(amount):
            arr.append("<empty>") 
        return
    except Exception as e:
        prepend_text_to_file("llm-research/session/cache/statistics.cache",f"Error in rule_syntax_analyzer.populate_empty_tag: {e}\n")
        return
    
def analyze_atomic(section1, section2):
    try: 
        #break down the sections str into an arr of atomic conditions
        atomic_arr_1 = atomic_section(section1)
        atomic_arr_2 = atomic_section(section2)

    
        if atomic_arr_1 == atomic_arr_2:
            return 1.0
        
        for atomic_condition_1 in atomic_arr_1:
           
            total_count = 0
            total_matching = 0

            for atomic_condition_2 in atomic_arr_2:
                subatomic_values_1 = sub_atomic_section(atomic_condition_1)
                len_1 = len(subatomic_values_1)
                subatomic_values_2 = sub_atomic_section(atomic_condition_2)
                len_2 = len(subatomic_values_2)
                    
                if len_1 != len_2:
                    diff = (len_2-len_1)
                    if diff > 0:
                        subatomic_values_1.extend(["<empty>"] * diff )
                    elif diff < 0:
                        subatomic_values_2.extend(["<empty>"] * (-diff ))
                # print(f"comparing {subatomic_values_1} to {subatomic_values_2}\n")

                for i in range(len(subatomic_values_1)):

                    #if set
                    if "{" in subatomic_values_1[i] and "}" in subatomic_values_1[i] :
                        if "{" in subatomic_values_2[i] and "}" in subatomic_values_2[i]:
                            total_matching += jaccard(subatomic_values_1[i], subatomic_values_2[i])
                            # print(f"jaccard triggered for: {subatomic_values_1[i]} || {subatomic_values_2[i]} == {jaccard(subatomic_values_1[i], subatomic_values_2[i])}")
                        else:
                            total_matching+=0 
                    else:
                        if(subatomic_values_1[i] == subatomic_values_2[i]):
                            total_matching += 1
                    total_count += 1

                #     value = total_matching / total_count
                # total_value += value
                        
        # print(f"\n\ntotal matching: {total_matching}      total count {total_count}  avg: {total_matching/total_count}")
        # print(f"{subatomic_values_1} <=> {subatomic_values_2} || matching {total_matching} total {total_count}")
        return total_matching/total_count
    
    except Exception as e:
        prepend_text_to_file("llm-research/session/cache/statistics.cache",f"Error in rule_syntax_analyzer.analyze_atomic: {e}\n")
        return 0


def main():
    gt_set = []
    # llm_set = []
    matching_rules = {}
    # llm_set = load_rules_from_file("jaccard-testing-rules.txt")
    # gt_set = load_rules_from_file("ground-truth-ABAC-rules/university-abac-rules.txt")
    
    llm_set = load_rules_from_file("ground-truth-ABAC-rules/university-abac-rules.txt")
    gt_set = load_rules_from_file("ground-truth-ABAC-rules/university-abac-rules.txt")


    rule_set_syntax_analyzer(gt_set, llm_set)

    # for key, value in matching_rules.items():
    #     print(f"{key} => {value}\n")
    # return


if __name__ == "__main__":
    main()