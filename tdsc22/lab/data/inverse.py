import json
import os
from itertools import islice
path = os.getcwd() + "/tdsc22/lab/data/enron1w_washed.json"
path_write = os.getcwd() + "/tdsc22/lab/data/enron10_invert.json"
with open(path, "r") as f:
    data = json.load(f)
data = dict(islice(data.items(), 10))

total = 0
invert = {}
for f, words in data.items():
    for w in words:
        if w not in invert.keys():
            invert[w] = []
        invert[w].append(f)
        total += 1

with open(path_write, "w", encoding="utf-8") as f:
    json.dump(invert, f)

print(total)