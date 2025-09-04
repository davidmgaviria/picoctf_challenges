import random
import string
import shutil
from pathlib import Path

start_path = Path("/home/ctf-player")
file_targets = ["flag_1of2.txt", "flag_2of2.txt"]
dir_targets = ["dir2"]

# Invisible characters to sprinkle in
invisible_chars = ["\u200b", "\u200c", "\u200d", "\u2060"]

def random_string(length=16, num_invisibles=4):
    s = [random.choice(string.ascii_letters) for _ in range(length)]
    for i in random.sample(range(length), min(num_invisibles, length)):
        s[i] = random.choice(invisible_chars)
    return ''.join(s)

# --- Step 1: Rename directories (deepest first) ---
dirs = [d for d in start_path.rglob("*") if d.is_dir() and d.name in dir_targets]
dirs.sort(key=lambda p: len(p.parts), reverse=True)

for d in dirs:
    new_name = f"{d.name}_{random_string(12, 4)}"
    new_path = d.with_name(new_name)
    print(f"Renaming dir: {repr(d)} -> {repr(new_path)}")
    shutil.move(str(d), str(new_path))

# --- Step 2: Collect and rename files ---
files = [f for f in start_path.rglob("*") if f.is_file() and f.name in file_targets]

for f in files:
    stem = f.stem
    suffix = f.suffix
    new_name = f"{stem}_{random_string(12, 4)}{suffix}"
    new_path = f.with_name(new_name)
    print(f"Renaming file: {repr(f)} -> {repr(new_path)}")
    shutil.move(str(f), str(new_path))

