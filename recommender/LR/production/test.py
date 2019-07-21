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
        result_list.append(item[0])
    return result_list

def sigmoid(x):
    return 1/(1 + math.exp(-x))

def predict_by_lr_coef(test_feature, lr_coef):
    sigmoid_func = np.frompyfunc(sigmoid,1,1)
    return sigmoid_func(np.dot(test_feature, lr_coef))

def run_check_core(test_feature, test_label, model, socre_func):
    predict_list = socre_func(test_feature, model)
    # get_auc(predict_list, test_label)
    # get_accuracy(predict_list, test_label)

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
    run_check_core(test_feature, test_label, lr_model, predict_by_lr_model)
    run_check_core(test_feature, test_label, lr_coef, predict_by_lr_coef)


if __name__ == "__main__":
    parent_path = os.path.dirname(os.path.dirname(__file__))
    run_check(parent_path + r'\data\test.txt', parent_path + r'\data\model_coef.txt', parent_path + r'\data\lr_model_file')