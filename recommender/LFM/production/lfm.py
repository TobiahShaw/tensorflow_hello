"""
author:TobiahShaw
date:2019-06-27
lfm,listen to the course on imooc.com
"""

import numpy as np
import sys, os
lib_path = os.path.dirname(os.path.dirname(__file__))
sys.path.append(lib_path)
import util.read as read
import operator

def lfm_train(train_data, f, alpha, beta, step):
    """
    train lfm model
    Args:
        train_data: train data for lfm
        f: user vector len, item vector len
        alpha: tregularation factor
        beta: learning rate
        step: iteration num
    Return:
        dict key: itemid, value: np.ndarray
        dict key: userid, value: np.ndarray
    """
    user_vec = {}
    item_vec = {}
    for step_index in range(step):
        for data_instance in train_data:
            userId, itemId, label = data_instance
            if userId not in user_vec:
                user_vec[userId] = init_model(f)
            if itemId not in item_vec:
                item_vec[itemId] = init_model(f)
        delta = label - model_predict(user_vec[userId], item_vec[itemId])
        for index in range(f):
            user_vec[userId][index] += beta * (delta * item_vec[itemId][index] - alpha * user_vec[userId][index])
            item_vec[itemId][index] += beta * (delta * user_vec[userId][index] - alpha * item_vec[itemId][index])
            # 衰减学习率
        beta = beta * 0.9
    return user_vec, item_vec

def init_model(f):
    return np.random.randn(f)

def model_predict(user_vector, item_vector):
    res = np.dot(user_vector, item_vector) / (np.linalg.norm(user_vector) * np.linalg.norm(item_vector))
    return res

def model_train_process():
    train_data = read.get_train_data(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))) + "\\recommender\\data\\ml-latest-small\\ratings.csv")
    user_vec, item_vec = lfm_train(train_data, 50, 0.01, 0.1, 50)

    recom_list = give_recommender(user_vec, item_vec, '24')
    ana_recom_result(train_data, "24", recom_list)


def give_recommender(user_vec, item_vec, userid):
    if userid not in user_vec:
        return []
    record = {}
    recom_list = []
    fix_num = 10
    user_vector = user_vec[userid]
    for itemid in item_vec:
        item_vector = item_vec[itemid]
        res = np.dot(user_vector, item_vector) / (np.linalg.norm(user_vector) * np.linalg.norm(item_vector))
        record[itemid] = res
    for tmp in sorted(record.items(), key=operator.itemgetter(1), reverse=True)[:fix_num]:
        recom_list.append((tmp[0], round(tmp[1], 3)))
    
    return recom_list


def ana_recom_result(train_data, userid, recom_list):
    item_info = read.get_item_info(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))) + "\\recommender\\data\\ml-latest-small\\movies.csv")
    for data_ins in train_data:
        tmp_userid, itemid, label = data_ins
        if tmp_userid == userid and label == 1:
            print(item_info[itemid])
    
    print("rec")

    for rec in recom_list:
        print(item_info[rec[0]])


if __name__ == "__main__":
    model_train_process()