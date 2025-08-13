import json

def main():
    # load info
    with open("/challenge/profile.json") as json_file:
        profile = json.load(json_file) 

    # assert username and profile exist
    if "username" not in profile:
        raise Exception("Username missing from profile.json")
    if "password" not in profile:
        raise Exception("Password missing from profile.json")

    # Login
    print("\n=========================================\nWelcome to the Online Banking Service!\n=========================================\n")
    print("Please enter your username & password to login.")
    user = input("Username: ")
    password = input("Password: ")

    if user == profile["username"] and password == profile["password"]:
        with open("/challenge/flag.txt") as file:
            flag = file.read()
        print("\nAuthenticating...\nWelcome %s!\n%s" % (user, flag))
    else:
        print("\nInvalid username or password")
    exit(0)


if __name__ == '__main__':
    main()



    

