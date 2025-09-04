from pwn import *
import json

def main():
    # Load JSON file into dictionary
    data = json.loads(open("metadata.json").read())

    # Connect to SSH server
    s = ssh("ctf-player", "ssh_host", password=data["password"])
    flag = s('cat flag/.flag.txt').decode()

    # Write flag to file
    with open("flag", "w") as w:
        w.write(flag)

if __name__ == "__main__":
    main()
