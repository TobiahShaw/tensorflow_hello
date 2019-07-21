import numpy as np
import os
from sklearn.linear_model import LogisticRegressionCV as LRCV


def train_lr_model(train_file, model_coef, model_file):
    """
    Agrs:
        train_file: process file for lr train
        model_coef: w1, w2 ...
        model_file: model_pkl
    """
    
    total_feature = 118
    train_label = np.genfromtxt(train_file, dtype=np.int32, delimiter=",",usecols=-1)
    feature_list = range(total_feature)
    train_feature = np.genfromtxt(train_file, dtype=np.int32, delimiter=",",usecols=feature_list)

    lr_cf = LRCV(Cs=[1, 10, 100], penalty="l2", tol=0.0001, max_iter=500, cv=5).fit(train_feature, train_label)
    scores = list(lr_cf.scores_.values())[0]
    print("diff:%s"%(",".join([str(ele) for ele in scores.mean(axis=0)])))
    print("Accuracy:%s (+-%0.2f)"%(scores.mean(), scores.std()*2))

    lr_cf = LRCV(Cs=[1, 10, 100], penalty="l2", tol=0.0001, max_iter=500, cv=5, scoring="roc_auc").fit(train_feature, train_label)
    scores = list(lr_cf.scores_.values())[0]
    print("diff:%s"%(",".join([str(ele) for ele in scores.mean(axis=0)])))
    print("AUC:%s (+-%0.2f)"%(scores.mean(), scores.std()*2))


if __name__ == "__main__":
    # recommender\LR\data\train.txt
    parent_path = os.path.dirname(os.path.dirname(__file__))
    train_lr_model(parent_path + r"\data\train.txt", "", "")