import requests 
import time

BASE_URL = "http://localhost:8000"
REGISTER_ENDPOINT = "/register"
LOGIN_ENDPOINT = "/login"
HEALTH_ENDPOINT = "/health"


def post_request(endpoint: str, data: dict):
    url = f"{BASE_URL}{endpoint}"
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        print(f"Request to {url} failed: {e}")
        exit(1)


def main():
	USERNAME = "admin"
	PASSWORD = "password"  # TODO: Use a stronger password in 

	# Attempt to ping health endpoint until it's active
	while True:
	    try:
	        resp = requests.get(f"{BASE_URL}{HEALTH_ENDPOINT}")
	        if resp.status_code == 200:
	            break
	    except requests.RequestException:
	        pass  # Ignore connection errors and keep trying
	    time.sleep(0.5)

	# Register & login admin
	register_data = { "username": USERNAME, "password": PASSWORD, "conf_password": PASSWORD }
	post_request(REGISTER_ENDPOINT, register_data)
	login_data = { "username": USERNAME, "password": PASSWORD }
	post_request(LOGIN_ENDPOINT, login_data)

if __name__ =='__main__':
	main()