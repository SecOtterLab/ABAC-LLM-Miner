def load_rules_from_file(path: str):
    rules = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("rule"):
                rules.append(line)
    return rules

def unwrap_rule(str) -> str:
    str = str.strip()
    str = str.replace("rule", "",1)
    str = str.replace("(", "")
    str = str.replace(")", "")

    return str

def split_rule(str):
    #split the string and convert to arr at ';'
    atomic_arr = [s.strip() for s in str.split(";")]
    
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

def printArr(arr):
    for x in arr:
        print(x)

import re
def sort_sets_in_line(text: str) -> str:
  ##AI GENERATED
    pattern = re.compile(r"\{([^}]*)\}")

    def sort_one(m: re.Match) -> str:
        items = m.group(1).split()
        # build (lowercased, original) pairs; sort by the pair (no lambda)
        pairs = [(s.casefold(), s) for s in items]
        pairs.sort()
        sorted_items = [orig for _, orig in pairs]
        return "{" + " ".join(sorted_items) + "}"

    return pattern.sub(sort_one, text)


        # rule(subCond; resCond; acts; cons)


#breaks down a set of rules into a data structure
# allows us to break down all the rules down once instead of every time we need to compare them
def rule_to_data_set(arr, arr_name):
    temp_arr = []
    for i in range ( len(arr)):
        unaltered_rule = arr[i]
        arr[i] = sort_sets_in_line(arr[i])
        arr[i] = unwrap_rule(arr[i])
        section_arr = split_rule(arr[i])
        id = f"{arr_name} {i}"
        temp_arr.append({"id": id, "subCond": section_arr[0] , "resCond": section_arr[1], "acts":str(section_arr[2]) , "cons":section_arr[3], "rule": unaltered_rule})

    return temp_arr

def atomic_section(str):

    # print(str)
    atomic_arr = [s.strip() for s in str.split(",")]
    #remove sets of brackets for easier parsing
    # for i in range (len(atomic_arr)):
    #     atomic_arr[i] = atomic_arr[i].replace("{", "").replace("}", "")

    atomic_arr.sort()
    # printArr(atomic_arr)
    # print(f"=================================\n")
    return atomic_arr

def sub_atomic_section(str):
    atomic_arr = [s.strip() for s in str.split(" ")]
    return atomic_arr

def str_set_to_arr(str):
    #take a string of set {r w x} and return an arr [r, w, x]
    atomic_arr = [s.strip().replace("{", "").replace("}","") for s in str.split(" ")]
    return atomic_arr

def tokenize(str):
    return str.replace("{", " ").replace("}", " ").split()
    
def jaccard(str1, str2):
    #arguements are string

    set1 = set(str_set_to_arr(str1))
    set2 = set(str_set_to_arr(str2))

    intersection = len(set1 & set2)
    union = len(set1 | set2)

    # jacc_value = float(intersection / union)

    return float(intersection / union)


def rule_set_compare(rules1, rules2, rule_map):
    arr1 = rule_to_data_set(rules1, "GT")
    arr2 = rule_to_data_set(rules2, "LLM")

    for rule1 in arr1:

        # print(gt_rule)
      

        rule_map[rule1['rule']] =("EMPTY_BY_DEFAULT", -1 )

        for rule2 in arr2:
            # print(llm_rule)
            sum_value = 0
            
            sum_value += analyze_atomic(rule1["subCond"], rule2["subCond"])
            sum_value += analyze_atomic(rule1["resCond"], rule2["resCond"])
            sum_value += jaccard(rule1["acts"], rule2["acts"])
            sum_value += analyze_atomic(rule1["cons"], rule2["cons"])


            avg_value = (sum_value/4)

            if avg_value > rule_map[rule1['rule']][1]:
                rule_map[rule1['rule']] = (rule2["rule"], avg_value)




    return rule_map


def populate_empty_tag(arr, amount):
    for _ in range(amount):
        arr.append("<empty>") 
    return

def analyze_atomic(section1, section2):

    #break down the sections str into an arr of atomic conditions
    atomic_arr_1 = atomic_section(section1)
    atomic_arr_2 = atomic_section(section2)

    max_value = -1


    for atomic_condition_1 in atomic_arr_1:
        for atomic_condition_2 in atomic_arr_2:
            subatomic_values_1 = sub_atomic_section(atomic_condition_1)
            len_1 = len(subatomic_values_1)
            subatomic_values_2 = sub_atomic_section(atomic_condition_2)
            len_2 = len(subatomic_values_2)
           
            total_count = 0
            total_matching = 0

            if len_1 != len_2:
                diff = (len_2-len_1)
                if diff > 0:
                    subatomic_values_1.extend(["<empty>"] * diff )
                elif diff < 0:
                    subatomic_values_2.extend(["<empty>"] * (-diff ))

            for i in range(len(subatomic_values_1)):

                
                if(subatomic_values_1[i] == subatomic_values_2[i]):
                    total_matching += 1
                total_count += 1

                value = total_matching / total_count

            if value > max_value:
                max_value = value
                


    

            # print(f"{subatomic_values_1} <=> {subatomic_values_2} || matching {total_matching} total {total_count}")
    return max_value


    


           



#TODO compare sets 


    return

def main():
    gt_set = []
    # llm_set = []
    matching_rules = {}
    llm_set = load_rules_from_file("jaccard-testing-rules.txt")
    gt_set = load_rules_from_file("ground-truth-ABAC-rules/university-abac-rules.txt")

    rule_set_compare(gt_set, llm_set, matching_rules)

    for key, value in matching_rules.items():
        print(f"{key} => {value}\n")
    return


if __name__ == "__main__":
    main()