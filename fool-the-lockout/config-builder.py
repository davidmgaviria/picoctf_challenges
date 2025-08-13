################################################################################
# Configure a box for the general ssh example challenge.
################################################################################

import sys
import os
import subprocess
import re
import json
import random

def main():
    try:
        # Generate user profile from seed =========================================
        seed = os.environ.get("SEED")
        if seed == "":
            print("Seed was not read from filesystem. Aborting.")
            sys.exit(1)

        # get credential dumplist & randomly select a user-password pair to use
        with open("/challenge/creds-dump.txt", "r") as file:      
            dumplist = [line.strip() for line in file.readlines()]
            user_password_tuple = random.choice(dumplist).split(";")

        # store password data
        profile = {"username":user_password_tuple[0], "password":user_password_tuple[1]}
        with open("/challenge/profile.json", "w") as json_file:
            json.dump(profile, json_file, indent=4)

        # Generate flag  =====================================
        flag = os.environ.get("FLAG")
        if flag == "":
            print("Flag was not read from environment. Aborting.")
            sys.exit(-1)
        else:
            # Get hash part
            flag_rand = re.search("{.*}$", flag)
            if flag_rand == None:
                print("Flag isn't wrapped by curly braces. Aborting.")
                sys.exit(-2)
            else:
                flag_rand = flag_rand.group()
                flag_rand = flag_rand[1:-1]
                flag_rand = flag_rand.zfill(8)

        flag = "picoCTF{f00l_7h4t_l1m1t3r_" + flag_rand + "}"
        with open("/challenge/flag.txt", "w") as f:
            f.write(flag)

        # Create and update metadata.json =====================================
        metadata = {}
        metadata['flag'] = str(flag)
        json_metadata = json.dumps(metadata)
        
        with open("/challenge/metadata.json", "w") as f:
            f.write(json_metadata)

        # =====================================================================

    except subprocess.CalledProcessError:
        print("A subprocess has returned an error code")
        sys.exit(1)

# =============================================================================

if __name__ == "__main__":
    main()

