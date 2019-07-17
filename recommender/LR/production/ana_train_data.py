import pandas as pd
import numpy as np
import os

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

def ana_train_data(input_train_file, input_test_file, out_train_file, out_test_file):
    """
    Args:
        input_train_file: train data input
        input_test_file: test data input
        out_train_file: train data output
        out_test_file: test data output
    """

if __name__ == "__main__":
    parent_path = os.path.dirname(os.path.dirname(__file__))
    train_data_df, test_data_df = get_input(parent_path + r'\data\adult.data', parent_path + r'\data\adult.test')
    print(train_data_df.shape)
    print(test_data_df.shape)