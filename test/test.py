import pandas as pd
import numpy as np
import pickle
import pytest
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sklearn.exceptions import NotFittedError

# import os,sys,inspect
# sys.path.insert(0,"..")

from src.generate_features import get_features, get_target
from src.train_model import get_mean, get_sd, train_test_split,train_model
from src.score_test_model import score_test_model
from src.eval_model import evaluate_model

def test_load_data():
    """Test if the loaded data is expected"""
    #expected first student
    expect = pd.read_csv("test/first_student.csv",header = None)
    idx = expect.iloc[:,1]
    expect= pd.Series(expect.iloc[:,2])
    expect.index = idx
    expected_GRE = int(expect[1])
    #loaded data
    data = pd.read_csv("data/Admission_Predict.csv")
    # print("expected student GRE", expected_GRE)
    #raise AssertionError if the GRE Score does not match
    
    assert expected_GRE == data['GRE Score'][0]

def test_get_features():
    """Test if get_features function select us correct column"""
    # load sample test data
    test_data = pd.read_csv("test/test_data.csv",index_col = 0)
    #actual features from get_features()
    X = get_features(test_data)
    X_colnames = X.columns.tolist()

    #expected
    expected_features =  ['GRE', 'TOEFL', 'University_rating', 'SOP', 'LOR', 'CGPA', 'Research', 'result']

    assert X_colnames == expected_features

def test_get_target():
    # load sample test data
    test_data = pd.read_csv("test/test_data.csv")
    #actual target from get_features()
    y = get_target(test_data,'result')
    # y_col = y.selected_columns
    #expected
    expected_target = test_data["result"][0]

    assert y == expected_target

def test_get_mean():
    test_data = {'x':[1,2,3],'y':[4,5,6]}
    test_df = pd.DataFrame(data=test_data)
    test_mean = get_mean(test_df)
    assert test_mean['x'] == 2 and test_mean['y'] == 5

def test_get_sd():
    test_data = {'x':[1,2,3],'y':[4,5,6]}
    test_df = pd.DataFrame(data=test_data)

    test_sd = get_sd(test_df)
    assert test_sd['x'] == 1 and test_sd['y'] == 1


def test_split_data():
    test_data = pd.read_csv("test/test_data10.csv",index_col = 0)
    X = test_data.drop(['result'],axis = 1)
    y = test_data['result']
    X, y = train_test_split(X,y,train_ratio = 0.8, test_ratio = 0.2, random_seed = 42)
    assert len(X['train']) == 8 and len(X['test'] == 2)


def test_model_type():
    """Test whether the trained model created from train_model script is of class xgboost."""
    # load sample test data
    data = pd.read_csv("test/test_to_train.csv", index_col = 0)
    methods = dict(logistic=LogisticRegression)
    # model to train
    method = 'logistic'
    # predefined arguments
    model_kwargs = {'get_features':{'selected_columns': ['GRE','TOEFL',"University_rating",'SOP', 'LOR' , 'CGPA' , 'Research']},
                'get_target':{'target':'result'},
                'train_test_split':{'train_ratio':0.8, 'test_ratio':0.2, 'random_seed':42}}
    # input column contains strings so expected to throw ValueError during model fit
    fit_bin = train_model(df=data, method=method, **model_kwargs)
    # check if the model type is right
    expected_type = "<class 'sklearn.linear_model.logistic.LogisticRegression'>"
    assert str(type(fit_bin)) == expected_type

def test_score_model():
    """test the function of score_test_model whether it gives correct prediction only 1 and 0"""
    
    df = pd.read_csv('test/test_data10.csv')
    X = df[['GRE', 'TOEFL', 'University_rating', 'SOP', 'LOR', 'CGPA', 'Research']]
    model_path = 'test/logreg.pkl'
   
    results = score_test_model(X_test = X, model_path = model_path,save_score=None)
    flag = 0
    for i in results:
        print("current i", i)
        if i != 0 and i != 1:
            flag = 1
    assert flag == 0

# def test_eval_model():
#     """test if the output was valid number (AUC and Accuracy are all between 0-1)"""
#     result = pd.read_csv("models/model_evaluation.csv")
#     flag = 0

#     if 'auc' not in result.columns:
#         flag = 1

#     if 'accuracy' not in result.columns:
#         flag = 1

#     print("auc is: ", result['auc'])
#     if result['auc']<0 or result['auc'] > 1:
#         flag = 1

#     if result['accuracy'] < 0  or result['accuracy'] > 1:
#         flag = 1

#     assert flag == 0 

