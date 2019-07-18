import pandas as pd
import numpy as np
import os
import operator

def get_input(input_train_file, input_test_file):
    """
    Args:
        input_train_file: train data input
        input_test_file: test data input
    Retrun:
        two pd.DataFrame of input
    """
    dtype_dict = {
        "age": np.int32,
        "education-num": np.int32,
        "capital-gain": np.int32,
        "capital-loss": np.int32,
        "hours-per-week": np.int32,
    }

    use_list = list(range(15))
    use_list.remove(2)

    train_data_df = pd.read_csv(input_train_file, sep=',',header=0,dtype=dtype_dict,na_values='?',usecols=use_list)
    train_data_df = train_data_df.dropna(axis=0, how='any')

    test_data_df = pd.read_csv(input_test_file, sep=',',header=0,dtype=dtype_dict,na_values='?',usecols=use_list)
    test_data_df = test_data_df.dropna(axis=0, how='any')

    return train_data_df, test_data_df

def label_trans(x):
    if x == "<=50K":
        return "0"
    elif x == ">50K":
        return "1"
    else:
        return "0"

def process_label_feature(label_str, df_in):
    df_in.loc[:,label_str] = df_in.loc[:,label_str].apply(label_trans)

def dict_trans(dict_in):
    out_dict = {}
    index = 0
    for comb in sorted(dict_in.items(), key=operator.itemgetter(1), reverse=True):
        out_dict[comb[0]] = index
        index+=1
    return out_dict

def dis_to_feature(x, feature_dict):
    result_list = [0] * len(feature_dict)
    if x in feature_dict:
        result_list[feature_dict[x]] = 1
    return ",".join(str(ele) for ele in result_list)

def process_dis_featrue(feature_str, train_data_df, test_data_df):
    origin_dict = train_data_df.loc[:, feature_str].value_counts().to_dict()
    feature_dict = dict_trans(origin_dict)
    train_data_df.loc[:, feature_str] = train_data_df.loc[:, feature_str].apply(dis_to_feature, args=(feature_dict,))
    test_data_df.loc[:, feature_str] = test_data_df.loc[:, feature_str].apply(dis_to_feature, args=(feature_dict,))

    print(train_data_df.loc[:3, :])
    print(feature_dict)

    return feature_dict

def ana_train_data(input_train_file, input_test_file, out_train_file, out_test_file):
    """
    Args:
        input_train_file: train data input
        input_test_file: test data input
        out_train_file: train data output
        out_test_file: test data output
    """
    train_data_df, test_data_df = get_input(input_train_file, input_test_file)
    label_str = 'label'
    process_label_feature(label_str, train_data_df)
    process_label_feature(label_str, test_data_df)
    # 离散化
    process_dis_featrue("workclass", train_data_df, test_data_df)

if __name__ == "__main__":
    parent_path = os.path.dirname(os.path.dirname(__file__))
    ana_train_data(parent_path + r'\data\adult.data', parent_path + r'\data\adult.test', parent_path + r'\data\train.csv', parent_path + r'\data\test.csv')