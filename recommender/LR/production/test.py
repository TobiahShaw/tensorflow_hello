import numpy as np
from sklearn.externals import joblib
import math
import os

def get_test_data(test_file):
    feature_num = 118
    test_label = np.genfromtxt(test_file, delimiter=",", usecols=-1)
    feature_list = range(feature_num)
    test_feature = np.genfromtxt(test_file, delimiter=",", usecols=feature_list)
    return test_feature, test_label

def predict_by_lr_model(test_feature, model):
    result_list = []
    prob_list = model.predict_proba(test_feature)
    for item in prob_list:
        result_list.append(item[1])
    return result_list

def sigmoid(x):
    return 1/(1 + math.exp(-x))

def predict_by_lr_coef(test_feature, lr_coef):
    sigmoid_func = np.frompyfunc(sigmoid,1,1)
    return sigmoid_func(np.dot(test_feature, lr_coef))

def get_auc(predict_list, test_label):
    """
    Args:
        predict_list: model_prodict_score_list
        test_label: label of test data

    AUC = (sum(pos_index) - post_num (post_num + 1) / 2)/(pos_num * neg_num)
    """
    total_list = []
    for index in range(len(predict_list)):
        predict_score = predict_list[index]
        label = test_label[index]
        total_list.append((label, predict_score))
    sorted_total_list = sorted(total_list, key=lambda ele:ele[1])
    neg_num = 0
    pos_num = 0
    count = 1
    total_pos_index = 0
    for comb in sorted_total_list:
        label, predict_score = comb
        if label == 0:
            neg_num += 1
        else:
            pos_num += 1
            total_pos_index += count
        count += 1
    auc_score = (total_pos_index - pos_num * (pos_num + 1)/2) / (neg_num * pos_num)
    print("auc:%0.5f"%auc_score)

def get_accuracy(predict_list, test_label):
    score_thr = 0.5
    right_num = 0
    for index in range(len(predict_list)):
        pre_score = predict_list[index]
        if pre_score >= score_thr:
            predict_label = 1
        else:
            predict_label = 0
        if predict_label == test_label[index]:
            right_num += 1
    accuracy_score = right_num / len(predict_list)
    print("accuracy:%0.5f"%accuracy_score)

def run_check_core(test_feature, test_label, model, socre_func):
    predict_list = socre_func(test_feature, model)

    get_auc(predict_list, test_label)
    get_accuracy(predict_list, test_label)

def run_check(test_file, model_coef_file, model_file):
    """
    Args:
        test_file: process test data for lr
        model_coef_file: w1, w2...
        model_file: model file
    """
    test_feature, test_label = get_test_data(test_file)
    lr_coef = np.genfromtxt(model_coef_file, delimiter=",")
    lr_model = joblib.load(model_file)
    print("model_file:")
    run_check_core(test_feature, test_label, lr_model, predict_by_lr_model)
    print("model_coef:")
    run_check_core(test_feature, test_label, lr_coef, predict_by_lr_coef)


if __name__ == "__main__":
    parent_path = os.path.dirname(os.path.dirname(__file__))
    run_check(parent_path + r'\data\test.txt', parent_path + r'\data\model_coef.txt', parent_path + r'\data\lr_model_file')