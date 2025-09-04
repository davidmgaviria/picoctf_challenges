################################################################################
# Configure a box for the general ssh example challenge.
################################################################################

import sys
import os
import subprocess
import re
import zlib
import json
import string
import random

def main():

    try:
        # Generate password from seed =========================================
        seed = os.environ.get("SEED")
        if seed == "":
            print("Seed was not read from filesystem. Aborting.")
            sys.exit(1)

        password = hex(zlib.crc32(seed.encode()))
        password = password[2:]

        with open("/challenge/password.txt", "w") as f:
          f.write(password)

        # =====================================================================

        # Split flag into 3 parts  ============================================
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

        flag = "picoCTF{dummy_flag_" + flag_rand + "}"

        # split the flag
        index = len(flag) // 2
        flag_1of2 = flag[:index]
        flag_2of2 = flag[index:]

        with open("/challenge/flag_1of2.txt", "w") as f:
            f.write(flag_1of2 + "\n")
        
        with open("/challenge/flag_2of2.txt", "w") as f:
            f.write(flag_2of2 + "\n")

        # =====================================================================

        # Create and update metadata.json =====================================

        metadata = {}
        metadata['flag'] = str(flag)
        metadata['password'] = str(password)
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

