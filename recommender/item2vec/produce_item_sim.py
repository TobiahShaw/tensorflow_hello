import os
import numpy as np
import operator

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

def cal_item_sim(item_vec, item_id, output_file, topK = 10):
    if item_id not in item_vec:
        return
    score = {}
    fix_item_vec = item_vec[item_id]
    for tmp_item_id in item_vec:
        if tmp_item_id == item_id:
            continue
        tmp_item_vec = item_vec[tmp_item_id]
        divider = np.linalg.norm(fix_item_vec) * np.linalg.norm(tmp_item_vec)
        if divider == 0:
            score[tmp_item_id] = 0
        else:
            score[tmp_item_id] = round(np.dot(fix_item_vec, tmp_item_vec) / divider, 3)
    fw = open(output_file, "w+", encoding='UTF-8')
    out_str = item_id + '\t'
    tmp_list = []
    for comb in sorted(score.items(), key=operator.itemgetter(1), reverse=True)[:topK]:
        tmp_list.append(comb[0] + '_' + comb[1])
    out_str += ";".join(tmp_list)
    fw.write(out_str + '\n')
    fw.close()
