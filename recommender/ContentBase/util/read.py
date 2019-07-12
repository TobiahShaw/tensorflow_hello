import os

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