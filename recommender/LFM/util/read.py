"""
author:TobiahShaw
date:2019-06-24
util function
"""
import os

def get_item_info(input_file):
    """
    get item info [title, genre]
    Args:
        input_file: item info file
    Return:
        a dict key : itemId, value: [title, genre]
    """
    if not os.path.exists(input_file):
        return {}

    item_info = {}
    
    fp = open(input_file,'r', encoding='UTF-8')

    linenum = 0
    for line in fp:
        if linenum == 0:
            linenum += 1
            continue
        item = line.strip().split(',')
        if len(item) < 3:
            continue
        elif len(item) == 3:
            itemId, title, genre = item[0], item[1], item[2]
        else:
            itemId = item[0]
            genre = item[-1]
            title = ",".join(item[1:-1])
        item_info[itemId] = [title, genre]
    fp.close()
    return item_info

def get_ave_score(input_file):
    """
    get item ave score
    Args:
        input_file: item info file
    Return:
        a dict key : itemId, ave score
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


if __name__ == "__main__":
    item_dict= get_item_info("D:\\WorkSpace\\python\\tensorflow_hello\\recommender\\data\\ml-latest-small\\movies.csv")
    print(len(item_dict))
    print(item_dict['1'])
    print(item_dict['11'])

    score_dict = get_ave_score("D:\\WorkSpace\\python\\tensorflow_hello\\recommender\\data\\ml-latest-small\\ratings.csv")
    print(len(score_dict))
    print(score_dict['31'])
