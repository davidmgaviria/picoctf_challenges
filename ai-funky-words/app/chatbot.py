import json
import time

from advancedInjectionFilter import PromptInjectionFilter
from openai import OpenAI


client = None
convo = []
allowed_queries = 100
limiter = {"rate": 1 }  # rate = number of requests per second


""" Simple rate limiting function to prevent request spam """
def rate_limit():
    global limiter

    curr_time = time.time()
    if "prev_time" not in limiter:
        limiter["prev_time"] = curr_time
        return

    delay = 1 / limiter["rate"]
    elapsed_time = curr_time - limiter["prev_time"]
    # delay 
    if elapsed_time < delay:
        print("Requests are only allowed every %s seconds, please wait" % delay)
        time.sleep(delay - elapsed_time)
    limiter["prev_time"] = time.time()



""" Input sanitization function, returns true if text is valid, false otherwise """
def input_filter():
    return True



""" Backend messaging to target AI """
def chat_with_bot(user_input):
    global convo
    convo.append({"role": "user", "content": user_input})
 
    response = client.chat.completions.create(
        model="gpt-4o-mini",   # or "gpt-3.5-turbo" / "gpt-4" / "gpt-4o-mini"
        messages=convo
    )
    reply = response.choices[0].message.content
    convo.append({"role": "assistant", "content": reply})
    return reply


""" Primary interface for user """
def main():
    global client, convo, allowed_queries

    # make sure we have api key
    try:
        api_key = open("/challenge/api-key.txt").read().strip()
        client = OpenAI(api_key=api_key)
    except FileNotFoundError:
        print("[Error] chatbot.py: No API key for OpenAI found! Please make sure an API key exists.")
        exit(1)
    except Exception as e:
        print("[Error] chatbot.py: issue with initalizing API key - %s" % e)
        exit(1)

    # make sure the model has a defined role
    try:
        context = open("/challenge/model-context.txt").read().strip()
        convo = [ {"role": "system", "content": context} ]   # initalize conversation
    except FileNotFoundError:
        print("[Error] chatbot.py: No model context given, challenge requires a model context.")
        exit(1)
    except Exception as e:
        print("[Error] chatbot.py: issue with initalizing model context - %s" % e)
        exit(1)

    # start app service
    pad = "="*50
    print(f"{pad}\n\t@@@ SIMPLE CHATBOT SERVICE 3.0 @@@\n{pad}")
    print("Welcome to the Simple Chatbot Service 3.0!\nFeel free to ask any question you have!\n\nRemaining queries: %s.\nType 'exit' or 'quit' to end conversation\n" % allowed_queries)
    
    # create a filter
    promptFilter = PromptInjectionFilter()

    while(allowed_queries > 0):
        user_input = input("[User]: ")

        if promptFilter.detect_injection(user_input) == True:
        # if injection detected, do not forward user query
            print("[Bot]: Im sorry but I cannot help you with that.")
        else:
        # process user input if filter deemed it safe
            sanitized_input = promptFilter.sanitize_input(user_input)
            if "exit" in sanitized_input.lower() or "quit" in sanitized_input.lower():
                print("[Bot]: Goodbye!") 
                exit(0)
            allowed_queries -= 1

            # apply rate limit &  get bot response
            rate_limit()
            response = chat_with_bot(sanitized_input)
            if "---GRANTING FLAG---" in response:
                flag = open("/challenge/flag.txt").read().strip()
                print("[Bot]: How did you bypass my defenses?!\nFlag\n%s" % flag)
                exit(0)
            else:
                print("[Bot]: %s" % response)

        print("** Remaining queries: %s **\n" % allowed_queries) 

    print("You have run out of allowed queries. Goodbye.")
    exit(0)


if __name__ == '__main__':
    main()



    

