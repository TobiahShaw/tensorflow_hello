"""
author:TobiahShaw
date:2019-06-24
util function,listen to the course on imooc.com
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

def get_train_data(input_file):
    """
    get train data for lfm model train
    Args:
        input_file: user item rating file
    Return:
        a list [(userid, itemid, label)]
    """
    if not os.path.exists(input_file):
        return []
    score_dict = get_ave_score(input_file)
    neg_dict = {}
    pos_dict = {}
    train_data = []
    score_thr = 4.0
    linenum = 0
    fp = open(input_file,'r', encoding='UTF-8')
    for line in fp:
        if linenum == 0:
            linenum += 1
            continue
        item = line.strip().split(',')
        if len(item) != 4:
            continue
        userId,itemId,rating = item[0], item[1], float(item[2])
        if userId not in pos_dict:
            pos_dict[userId] = []
        if userId not in neg_dict:
            neg_dict[userId] = []
        if rating >= score_thr:
            pos_dict[userId].append((itemId, 1))
        else:
            score = score_dict.get(itemId, 0)
            neg_dict[userId].append((itemId, score))
    fp.close()
    for userId in pos_dict:
        data_num = min(len(pos_dict[userId]), len(neg_dict.get(userId,[])))
        if data_num == 0:
            continue
        train_data += [(userId, tmp[0], tmp[1]) for tmp in pos_dict[userId][:data_num]]
        sorted_neg_list = sorted(neg_dict[userId], key=lambda element:element[1], reverse=True)[:data_num]
        train_data += [(userId, tmp[0], 0) for tmp in sorted_neg_list]
    return train_data

if __name__ == "__main__":
    item_dict= get_item_info(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))) + "\\recommender\\data\\ml-latest-small\\movies.csv")
    print(len(item_dict))
    print(item_dict['1'])
    print(item_dict['11'])

    score_dict = get_ave_score(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))) + "\\recommender\\data\\ml-latest-small\\ratings.csv")
    print(len(score_dict))
    print(score_dict['31'])

    train_data = get_train_data(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))) + "\\recommender\\data\\ml-latest-small\\ratings.csv")
    print(len(train_data))
    print(train_data[:20])
