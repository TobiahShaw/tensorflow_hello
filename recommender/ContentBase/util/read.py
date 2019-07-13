import os
import operator

def get_ave_score(input_file):
    """
    get item ave score
    Args:
        input_file: user item rating file
    Return:
        a dict key : itemId, value : ave score
    """
    if not os.path.exists(input_file):
        return {}

    score_dict = {}
    record_dict = {}
    
    fp = open(input_file,'r', encoding='UTF-8')
    linenum = 0
    for line in fp:
        if linenum == 0:
            linenum += 1
            continue
        item = line.strip().split(',')
        if len(item) != 4:
            continue

        itemId,rating = item[1], item[2]
        if itemId not in record_dict:
            record_dict[itemId] = [0, 0.0]
        record_dict[itemId][0] += 1
        record_dict[itemId][1] += float(rating)
    fp.close()
    for itemId in record_dict:
        score_dict[itemId] = round(record_dict[itemId][1] / record_dict[itemId][0],3)

    return score_dict

def get_item_category(ave_score, input_file):
    """
    get item category
    Args:
        ave_score: item average score
        input_file: user item info file
    Return:
        a dict key : itemId, value : a dict key : category,value: ratio
        a dict key : category, value: [item1, item2....]
    """
    if not os.path.exists(input_file):
        return {}, {}
    
    item_cate={}
    record = {}
    cate_item_scort = {}

    topK = 100

    fp = open(input_file,'r', encoding='UTF-8')
    linenum = 0
    for line in fp:
        if linenum == 0:
            linenum += 1
            continue
        item = line.strip().split(',')
        if len(item) < 3:
            continue
        itemid = item[0]
        cate_str = item[-1]
        cate_list = cate_str.strip().split('|')
        ratio = round(1/len(cate_list), 3)
        if itemid not in item_cate:
            item_cate[itemid] = {}
        for fix_cate in cate_list:
            item_cate[itemid][fix_cate] = ratio
    fp.close()
    for tmp_item_id in item_cate:
        for cate in item_cate[tmp_item_id]:
            if cate not in record:
                record[cate] = {}
            item_ave_score = ave_score.get(tmp_item_id, 0)
            record[cate][tmp_item_id] = item_ave_score
    for cate in record:
        if cate not in cate_item_scort:
            cate_item_scort[cate] = []
        for comb in sorted(record[cate].items(), key=operator.itemgetter(1), reverse=True)[:topK]:
            cate_item_scort[cate].append(comb[0])
    return item_cate, cate_item_scort

if __name__ == "__main__":
    score_dict = get_ave_score(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))) + "\\recommender\\data\\ml-latest-small\\ratings.csv")
    print(len(score_dict))
    print(score_dict['31'])

    print("-" * 20)
    item_cate, cate_item_scort = get_item_category(score_dict, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))) + "\\recommender\\data\\ml-latest-small\\movies.csv")
    print(item_cate["1"])

    print("-" * 20)
    print(cate_item_scort["Children"])
