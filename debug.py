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
        temp_arr.append({"id": id, "subCond": section_arr[0] , "resCond": section_arr[1], "acts":section_arr[2] , "cons":section_arr[3], "rule": unaltered_rule})

    return temp_arr

def atomic_section(str):
    atomic_arr = [s.strip() for s in str.split(",")]
    #remove sets of brackets for easier parsing
    # for i in range (len(atomic_arr)):
    #     atomic_arr[i] = atomic_arr[i].replace("{", "").replace("}", "")

    return atomic_arr

def sub_atomic_section(str):
    atomic_arr = [s.strip() for s in str.split(" ")]
    return atomic_arr

def tokenize(str):
    return str.replace("{", " ").replace("}", " ").split()
    
def jaccard_calc_totals(gt_arr, llm_arr):

    gt_tokens = []
    llm_tokens = []
    for gt in gt_arr:
        temp = tokenize(gt)
        for str in temp:
            gt_tokens.append(str)


    for llm in llm_arr:
        temp = tokenize(llm)
        for str in temp:
            llm_tokens.append(str)

  
    gt_set = set(gt_tokens)
    llm_set = set(llm_tokens)

    intersection = gt_set.intersection(llm_set)
    union = gt_set.union(llm_set)
    # print(f"{len(intersection)},  {len(union)}")
    return (len(intersection), len(union))


def rule_set_compare(gt_set, llm_set, rule_map):
    gt_arr = rule_to_data_set(gt_set, "GT")
    llm_arr = rule_to_data_set(llm_set, "LLM")

    for gt_rule in gt_arr:

        # print(gt_rule)
        gt_subCond = atomic_section (gt_rule["subCond"])
        gt_resCond = atomic_section(gt_rule["resCond"])
        gt_acts = atomic_section(gt_rule["acts"])
        gt_cons = atomic_section(gt_rule["cons"])

        rule_map[gt_rule['rule']] =("EMPTY_BY_DEFAULT", -1 )

        for llm_rule in llm_arr:
            # print(llm_rule)
            intersection_count = 0
            union_count= 0
            llm_subCond = atomic_section (llm_rule["subCond"])
            llm_resCond = atomic_section(llm_rule["resCond"])
            llm_acts = atomic_section(llm_rule["acts"])
            llm_cons = atomic_section(llm_rule["cons"])
            

            # print(f"{gt_subCond} <=> {llm_subCond}\n")
            inter, union = jaccard_calc_totals(gt_subCond, llm_subCond )
            intersection_count += inter
            union_count += union


            # print(f"{gt_resCond} <=> {llm_resCond}\n")
            inter, union = jaccard_calc_totals(gt_resCond, llm_resCond )
            intersection_count += inter
            union_count += union
            
            # print(f"{gt_acts} <=> {llm_acts}\n")
            inter, union = jaccard_calc_totals(gt_acts, llm_acts )
            intersection_count += inter
            union_count += union

            # print(f"{gt_cons} <=> {llm_cons}\n")
            inter, union = jaccard_calc_totals(gt_cons, llm_subCond )
            intersection_count += inter
            union_count += union

            jacc_val= intersection_count/union_count
            # print(f"inter: {intersection_count} union: {union_count} jacc: {jacc_val}")
            # print("===============================")
            
            if jacc_val > rule_map[gt_rule['rule']][1]:
                rule_map[gt_rule['rule']] = (llm_rule["rule"], jacc_val)




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