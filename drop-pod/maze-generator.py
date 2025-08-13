import os
import shutil
import random

start = "/home/ctf-player"
min_split = 3
max_split = 8
constructed_paths = []


# generate maze
os.chdir(start)
trunks = random.randint(min_split,max_split)
for i in range(trunks):
    trunk_path = os.path.join(start, f"t{i}")

    branches = random.randint(min_split,max_split)
    for j in range(branches):
        branch_path = os.path.join(trunk_path, f"b{j}")

        leaves = random.randint(min_split,max_split)
        for k in range(leaves):
            leaf_path = os.path.join(branch_path, f"lf{k}")
            constructed_paths.append(leaf_path)
            os.makedirs(leaf_path, exist_ok=True)
        

# move flag
chosen_path = random.choice(constructed_paths)
shutil.move("flag.txt", chosen_path)


