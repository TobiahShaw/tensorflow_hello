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
    train_data = read.get_train_data("D:\\WorkSpace\\python\\tensorflow_hello\\recommender\\data\\ml-latest-small\\ratings.csv")
    user_vec, item_vec = lfm_train(train_data, 50, 0.01, 0.1, 50)

    print(user_vec["1"])
    print(item_vec["24"])

if __name__ == "__main__":
    model_train_process()