
import random

name_list = [line.strip() for line in open("names.txt", "r")]
password_list = [line.strip() for line in open("10k-most-common.txt", "r")]

output = ""
count = 0
for i in range(1500):
    username = random.choice(name_list)
    password = random.choice(password_list)
    line = f"{username};{password}\n"
    if line.count(';') == 1:
        output += line
        count += 1

filename = "creds-dump.txt"
with open(filename, "w") as file:
    file.write(output)

print("Wrote %d username-password combos to %s" % (count, filename))