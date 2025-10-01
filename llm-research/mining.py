import datetime
from acl_tools import compare_acl, generate_acl, rule_semantic_analyzer
from myabac import parse_abac_file
from rule_syntax_analyzer import rule_set_syntax_analyzer
from helper_functions import *

def prompt_generator(gt_acl_file, attribute_data_file, attribute_data_description_file, prompt_file, complete_request_file , comparison_file ):
    try: 
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
            sections["## CURRENT_RULES ##"]= "llm-research/session/session/session-llm-response.txt"
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

    except Exception as e:
            prepend_text_to_file("llm-research/session/cache/statistics.cache", f"Error in helper_functions.prompt_generator: {e}\n")
            return

def iterate_api_requests(gt_acl_file,gt_abac_rules_file,  attribute_data_file, attribute_data_description_file, max_num_it, api_call, model, num_ctx):
    try:
        # generated file #: declare the location on the complete request being made
        # this file should contain everyhting we are feeding the LLM to make the rules.
        complete_request_file = "prompts/complete-prompt.txt"
        prompt_file = "prompts/initial-starting-prompt.txt"
        comparison_file ="prompts/empty.txt"

        prompt_generator(gt_acl_file, attribute_data_file, attribute_data_description_file, prompt_file, complete_request_file , comparison_file )
        
        append_from_file("llm-research/session/output/complete-initial-prompt.txt", complete_request_file )
        print("ITERATING API CALLS..")
        
        is_match = False
        counter = 0
        print(f"running iteration {counter} ...")

        session_abac_file ="llm-research/session/session/session-abac.txt"
        session_acl_file="llm-research/session/session/session-ACL.txt"
        session_comparison_file="llm-research/session/session/session-comparison.txt"
        session_llm_response_file="llm-research/session/session/session-llm-response.txt"

        #The initial complete prompt file, to make the initial request

        complete_request = read_entire_file(complete_request_file)

        timestamp_start = datetime.datetime.now()
        # The api_call function will return text of the response.
        if model is None and num_ctx is None:
            payload_text = api_call(complete_request)
        else:
            payload_text = api_call(complete_request, model, num_ctx)

        timestamp_end = datetime.datetime.now()
        elapsed_seconds = (timestamp_end - timestamp_start)

        #output the abac rules to a file for testing
        if not payload_text or not payload_text.strip():
            print(f"skipping iteration: payload not received\n")
            prepend_text_to_file("llm-research/session/cache/statistics.cache", f"skipping iteration: payload not received\n")
            # exit
        else:
            print("payload recieved...")
            with open(session_llm_response_file, "w", encoding="utf-8") as of:
                of.write(payload_text)

            # ensure_rule_file(session_llm_response_file)

        stats_text = (f"\n\niteration : {counter},"
                    f"\n  seconds_elapsed : {elapsed_seconds},"
        )    
        append_to_file( "llm-research/session/output/statistics.txt", stats_text )

        is_match = create_session_data(session_abac_file, attribute_data_file, session_llm_response_file, session_acl_file, gt_acl_file, session_comparison_file)

        #maps one rule from the llm to all rules in the gt
        syntax_jacc_avg, syntax_map = rule_set_syntax_analyzer(gt_abac_rules_file, session_llm_response_file)
        write_map_to_file("llm-research/session/session/session-llm-to-gt-syntax.txt", syntax_map)
        #generate semantic comparison
        #maps one rule from the llm to all rules in the gt
        semantic_jacc_avg , semantic_map = rule_semantic_analyzer(gt_abac_rules_file, session_llm_response_file, attribute_data_file)
        write_map_to_file("llm-research/session/session/session-llm-to-gt-semantic.txt", semantic_map )

        #maps one rule from the gt to all rules in the llm
        syntax_jacc_avg_2, syntax_map_2 = rule_set_syntax_analyzer(session_llm_response_file, gt_abac_rules_file)
        write_map_to_file("llm-research/session/session/session-gt-to-llm-syntax.txt", syntax_map_2)
        #generate semantic comparison
        #maps one rule from the gt to all rules in the llm
        semantic_jacc_avg_2 , semantic_map_2 = rule_semantic_analyzer(session_llm_response_file, gt_abac_rules_file, attribute_data_file)
        write_map_to_file("llm-research/session/session/session-gt-to-llm-semantic.txt", semantic_map_2 )

        

        
        stats_text = (f"\n  syntax_jacc_avg : {syntax_jacc_avg},"
                        f"\n  semantic_jacc_avg : {semantic_jacc_avg},"
        )
        
        append_to_file( "llm-research/session/output/statistics.txt", stats_text )

        x_syntax_jacc_avg = (syntax_jacc_avg + syntax_jacc_avg_2)/2
        x_semantic_jacc_avg = (semantic_jacc_avg + semantic_jacc_avg_2)/2

        stats_text = (f"\n  x_syntax_jacc_avg   : {x_syntax_jacc_avg},"
                      f"\n  x_semantic_jacc_avg : {x_semantic_jacc_avg}"
        )
        append_to_file( "llm-research/session/output/statistics.txt", stats_text )

        write_to_logs(counter)

        counter +=1
        
        while( counter < max_num_it):
            try:
                print(f"running iteration {counter} ...")

                prompt_file = ("prompts/subsequent-starting-prompt.txt")
                prompt_generator(gt_acl_file, attribute_data_file, attribute_data_description_file,prompt_file, complete_request_file , session_comparison_file )

                complete_request = read_entire_file(complete_request_file)

                timestamp_start = datetime.datetime.now()
                # The api_call function will return text of the response.
                if model is None and num_ctx is None:
                    payload_text = api_call(complete_request)
                else:
                    payload_text = api_call(complete_request, model, num_ctx)
                
                timestamp_end = datetime.datetime.now()
                elapsed_seconds = (timestamp_end - timestamp_start)

                #output the abac rules to a file for testing
                if(payload_text is None):
                    print(f"skipping iteration: payload not received\n")
                    counter +=1
                    continue
                else:
                    print("payload recieved...")
                    with open(session_llm_response_file, "w", encoding="utf-8") as of:
                        of.write(payload_text)

                    # ensure_rule_file(session_llm_response_file)

                stats_text = (f"\n\niteration : {counter},"
                            f"\n  seconds_elapsed : {elapsed_seconds},"
                )
                
                append_to_file( "llm-research/session/output/statistics.txt", stats_text )
                
                is_match = create_session_data(session_abac_file, attribute_data_file, session_llm_response_file, session_acl_file, gt_acl_file, session_comparison_file)

                #maps one rule from the llm to all rules in the gt
                syntax_jacc_avg, syntax_map = rule_set_syntax_analyzer(gt_abac_rules_file, session_llm_response_file)
                write_map_to_file("llm-research/session/session/session-llm-to-gt-syntax.txt", syntax_map)
                #generate semantic comparison
                #maps one rule from the llm to all rules in the gt
                semantic_jacc_avg , semantic_map = rule_semantic_analyzer(gt_abac_rules_file, session_llm_response_file, attribute_data_file)
                write_map_to_file("llm-research/session/session/session-llm-to-gt-semantic.txt", semantic_map )

                #maps one rule from the gt to all rules in the llm
                syntax_jacc_avg_2, syntax_map_2 = rule_set_syntax_analyzer(session_llm_response_file, gt_abac_rules_file)
                write_map_to_file("llm-research/session/session/session-gt-to-llm-syntax.txt", syntax_map_2)

                #generate semantic comparison
                #maps one rule from the gt to all rules in the llm
                semantic_jacc_avg_2 , semantic_map_2 = rule_semantic_analyzer(session_llm_response_file, gt_abac_rules_file, attribute_data_file)
                write_map_to_file("llm-research/session/session/session-gt-to-llm-semantic.txt", semantic_map_2 )

                


                stats_text = (f"\n  syntax_jacc_avg : {syntax_jacc_avg},"
                            f"\n  semantic_jacc_avg : {semantic_jacc_avg}"
                )
                append_to_file( "llm-research/session/output/statistics.txt", stats_text )


                x_syntax_jacc_avg = (syntax_jacc_avg + syntax_jacc_avg_2)/2
                x_semantic_jacc_avg = (semantic_jacc_avg + semantic_jacc_avg_2)/2

                stats_text = (f"\n  x_syntax_jacc_avg   : {x_syntax_jacc_avg},"
                              f"\n  x_semantic_jacc_avg : {x_semantic_jacc_avg}"
                )
                append_to_file( "llm-research/session/output/statistics.txt", stats_text )

                write_to_logs(counter)

                counter +=1

            except Exception as e:
                prepend_text_to_file("llm-research/session/cache/statistics.cache", f"Error in helper_functions.iterate_api_requests.iteration_step: {e}\n")
                write_to_logs(counter)
          
                continue

    except Exception as e:
        prepend_text_to_file("llm-research/session/cache/statistics.cache",f"Error in helper_functions.iterate_api_requests.initial_step: {e}\n")
        write_to_logs(counter)
        pass

def create_session_data(session_abac_file, attribute_data_file, session_response, llm_acl_file, gt_acl_file, session_comparison_file):
            
    try:
        #clear the file for the iteration
        clear_file(session_abac_file)
        # write the abac policy (llm version that has no rules) into the session abac file
        try:
            append_from_file(session_abac_file, attribute_data_file)

        except:
            print("error 1")
       
        # user attribute data
        try:
            append_to_file(session_abac_file, "\n\n#------------------------------------------------------------\n\n")
            append_to_file(session_abac_file, "#ABAC Rules")
            append_to_file(session_abac_file, "\n\n#------------------------------------------------------------\n\n")
        except:
            print("error 2")



        rules_text = read_entire_file(session_response)
        if not rules_text.strip():
            raise ValueError(f"LLM rules file is empty: {session_response}")
        append_to_file(session_abac_file, rules_text + "\n")

        # print(file_to_text(session_abac_file))
        try:
            user2, res2, rule2 = parse_abac_file(session_abac_file)
        except:
            print("error 3")

        try:

            if user2 is None or res2 is None:
                raise ValueError("parse_abac_file returned invalid user/resource structures")
            if not rule2:
                raise ValueError("No rules parsed from session_abac_file")

            generate_acl(user2, res2, rule2, llm_acl_file)

        except:
            print("error 4")

        try:
            stats_text, debug_text, is_match, _ = compare_acl(gt_acl_file, llm_acl_file)
            append_to_file("llm-research/session/output/statistics.txt", stats_text)
            write_to_file(session_comparison_file, debug_text)
            return is_match
        except:
            print("error 5")

    except Exception as e:

        stats_text, debug_text, is_match, _ = compare_acl(gt_acl_file, llm_acl_file)
        append_to_file("llm-research/session/output/statistics.txt", stats_text)
        write_to_file(session_comparison_file, debug_text)
        prepend_text_to_file("llm-research/session/cache/statistics.cache",
                             f"Error in helper_functions.iterate_api_requests.create_session_data: {e}\n")
        return False
        
def write_to_logs(num_it):
    try:
        divider_text = (f"\n===============================================================\nITERATION : {num_it}\n===============================================================\n")
        
        prepend_file("llm-research/session/cache/complete-prompt.cache", "prompts/complete-prompt.txt")
        prepend_text_to_file("llm-research/session/cache/complete-prompt.cache", divider_text)

        prepend_file("llm-research/session/cache/session-abac.cache", "llm-research/session/session/session-abac.txt")
        prepend_text_to_file("llm-research/session/cache/session-abac.cache", divider_text)

        prepend_file("llm-research/session/cache/session-ACL.cache", "llm-research/session/session/session-ACL.txt")
        prepend_text_to_file("llm-research/session/cache/session-ACL.cache", divider_text)

        prepend_file("llm-research/session/cache/session-comparison.cache", "llm-research/session/session/session-comparison.txt")
        prepend_text_to_file("llm-research/session/cache/session-comparison.cache", divider_text)

        prepend_file("llm-research/session/cache/session-llm-response.cache", "llm-research/session/session/session-llm-response.txt")
        prepend_text_to_file("llm-research/session/cache/session-llm-response.cache", divider_text)
        
        prepend_file("llm-research/session/output/generated-rules.txt", "llm-research/session/session/session-llm-response.txt")
        prepend_text_to_file("llm-research/session/output/generated-rules.txt", divider_text)

        prepend_file("llm-research/session/cache/session-gt-to-llm-semantic.cache", "llm-research/session/session/session-gt-to-llm-semantic.txt")
        prepend_text_to_file("llm-research/session/cache/session-gt-to-llm-semantic.cache", divider_text)

        prepend_file("llm-research/session/cache/session-gt-to-llm-syntax.cache", "llm-research/session/session/session-gt-to-llm-syntax.txt")
        prepend_text_to_file("llm-research/session/cache/session-gt-to-llm-syntax.cache", divider_text)

        prepend_file("llm-research/session/cache/session-llm-to-gt-semantic.cache", "llm-research/session/session/session-llm-to-gt-semantic.txt")
        prepend_text_to_file("llm-research/session/cache/session-llm-to-gt-semantic.cache", divider_text)

        prepend_file("llm-research/session/cache/session-llm-to-gt-syntax.cache", "llm-research/session/session/session-llm-to-gt-syntax.txt")
        prepend_text_to_file("llm-research/session/cache/session-llm-to-gt-syntax.cache", divider_text)
        
        prepend_file("llm-research/session/cache/statistics.cache", "llm-research/session/output/statistics.txt")
        prepend_text_to_file("llm-research/session/cache/statistics.cache", divider_text)
        
        return
    except Exception as e:
            prepend_text_to_file("llm-research/session/cache/statistics.cache",f"Error in helper_functions.iterate_api_requests.write_to_logs: {e}\n")

            return False

    