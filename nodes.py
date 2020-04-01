from glob import glob

nodes = {}

for node in glob("nodes/*.py"):
    with open(node, "r") as f:
        exec(f.read())
