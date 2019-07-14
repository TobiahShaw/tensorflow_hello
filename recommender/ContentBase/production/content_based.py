import os
import operator

def get_up(item_cate, input_file):
    """
    Args:
        item_cate: key : itemid, value : a dict key : category, value: score
        input_file: user rating file
    Return: 
        a dict : key userid value [(category, ratio)]
    """
    if not os.path.exists(input_file):
        return {}
    record = {}
    up = {}
    fp = open(input_file,'r', encoding='UTF-8')
    linenum = 0
    score_thr = 4.0
    topK = 2
    for line in fp:
        if linenum == 0:
            linenum += 1
            continue
        item = line.strip().split(',')
        if len(item) < 4:
            continue
        userid, itemid, rating, timestep = item[0], item[1], float(item[2]), int(item[3])
        if rating < score_thr:
            continue
        if itemid not in item_cate:
            continue
        time_score = get_time_score(timestep)
        if userid not in record:
            record[userid] = {}
        for fix_cate in item_cate[itemid]:
            if fix_cate not in record[userid]:
                record[userid][fix_cate] = 0
            record[userid][fix_cate] += rating * time_score * item_cate[itemid][fix_cate]
    fp.close()
    for userid in record:
        if userid not in up:
            up[userid] = []
        total_score = 0
        for comb in sorted(record[userid].items(), key=operator.itemgetter(1), reverse=True)[:topK]:
            up[userid].append((comb[0], comb[1]))
            total_score += comb[1]
        for index in range(len(up[userid])):
            up[userid][index][1] = round(up[userid][index][1]/ total_score, 3)
    return up
def get_time_score(timestep):
    fix_time_stamp = 800000000
    total_sec = 24*60*60
    delta = (timestep - fix_time_stamp) / total_sec
    return round(1 / (1 + delta), 3)

def recom(cate_item_sort, up, userid, topK = 10):
    """
    Args:
        cate_item_sort: cate item reversed sort
        up: user profile
        userid: user's id
        topK: recom num
    """
    if userid not in up:
        return{}
    recom_result = {}
    if userid not in recom_result:
        recom_result[userid] = []
    for comb in up[userid]:
        category, ratio = comb
        num = int(topK * ratio) + 1
        if category not in cate_item_sort:
            continue
        recom_list =  cate_item_sort[category] [:num]
        recom_result[userid] += recom_list
    return recom_result
