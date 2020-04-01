from glob import glob

groups = {}

for group in glob("groups/*.py"):
    with open(group, "r") as f:
        exec(f.read())
