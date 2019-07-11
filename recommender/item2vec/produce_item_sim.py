import os
import numpy as np

def load_item_vec(input_file):
    if not os.path.exists(input_file):
        return {}
    linenum = 0
    item_vec = {}
    fp = open(input_file, "r", encoding='UTF-8')
    for line in fp.readlines():
        if linenum == 0:
            linenum += 1
            continue
        item = line.strip().split()
        if len(item) < 129:
            continue
        itemid = item[0]
        if itemid == "</s>":
            continue
        item_vec[item] = np.array([float(ele) for ele in item[1:]])
    fp.close()
    return item_vec
