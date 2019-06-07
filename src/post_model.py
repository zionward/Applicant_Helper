import logging
import argparse
import yaml
import os
from sklearn import metrics

import pickle


import sklearn
import pandas as pd
import numpy as np
import math

from sklearn.metrics import accuracy_score, recall_score, roc_auc_score, confusion_matrix, f1_score

#from load_data import load_data
from generate_features import get_features, get_target
from train_model import train_test_split, get_mean, get_sd,normalize_features
from score_model import get_new_student, normalize_new_student
from sklearn.linear_model import LogisticRegression

logger = logging.getLogger(__name__)


def binary_search_GRE(stud_to_pred, logreg,X_mean,X_sd):
    new_GRE = stud_to_pred.iloc[0]['GRE']
    stud_to_pred2 =stud_to_pred
    stud_to_pred2["GRE"] = (340 - X_mean["GRE"])/X_sd["GRE"]
    y_new = logreg.predict(stud_to_pred2)
    #cur_score = stud_to_pred.iloc[0]['GRE']
    #Base case: check if full grade in this project can be admit
    if y_new[0] == 0: 
        print("Cannot get admitted by improving only this subject. Fighting!")
        return 340
    low_pred = 0
    low_score = new_GRE
    high_pred = y_new[0]
    high_score = 340
    diff = high_score - low_score
    while diff > 1:
        mid_score = low_score + math.floor(diff/2)
        stud_to_pred2['GRE'] = (mid_score - X_mean["GRE"])/X_sd["GRE"]
        y_new = logreg.predict(stud_to_pred2)
        if y_new[0]*high_pred < 1:#mid is not admitted, go to upper part
            low_score = mid_score
        else: #mid is admitted, go to lower part
            high_score = mid_score
        diff = high_score - low_score

    return high_score

def binary_search_TOEFL(stud_to_pred, logreg,X_mean,X_sd):
    new_TOEFL = stud_to_pred.iloc[0]['TOEFL']
    stud_to_pred2 =stud_to_pred
    stud_to_pred2["TOEFL"] = (120 - X_mean["TOEFL"])/X_sd["TOEFL"]
    y_new = logreg.predict(stud_to_pred2)
    #cur_score = stud_to_pred["TOEFL"][0]
    #Base case: check if full grade in this project can be admit
    if y_new[0] == 0: 
        print("Cannot get admitted by improving only this subject. Fighting!")
        return 120

    low_pred = 0
    low_score = new_TOEFL
    high_pred = y_new[0]
    high_score = 120
    diff = high_score - low_score
    while diff > 1:
        mid_score = low_score + math.floor(diff/2)
        stud_to_pred2['TOEFL']= (mid_score - X_mean["TOEFL"])/X_sd["TOEFL"]
        y_new = logreg.predict(stud_to_pred2)
        if y_new[0]*high_pred < 1:#mid is not admitted, go to upper part
            low_score = mid_score
        else: #mid is admitted, go to lower part
            high_score = mid_score
        diff = high_score - low_score

    return high_score

def post_model(X,new_pred, option, model_path, **kwargs):
    logger.debug("Binary Search for target score")
    with open(model_path, "rb") as f:
        logreg = pickle.load(f)
    
    if "get_features" in kwargs:
        new_pred = get_features(new_pred,**kwargs["get_features"])
        X = get_features(X,**kwargs["get_features"])
    else:
        new_pred = new_pred
        X = X
   
    X_mean = get_mean(X)
    X_sd = get_sd(X)
    if option == 'GRE':
        new_score= binary_search_GRE(new_pred,logreg,X_mean,X_sd)
    elif option == 'TOEFL':
        new_score = binary_search_TOEFL(new_pred,logreg,X_mean,X_sd)
    else:
        raise ValueError("Please enter GRE or TOEFL.")
    return new_score
    

def run_post_model(args):
    with open(args.config, "r") as f:
        config = yaml.load(f)

    if args.option is not None:
        option = args.option
    else:
        raise ValueError("Please enter GRE or TOEFL")

    #online new student
    if args.input is not None:
        stud_to_pred= pd.read_csv(args.input, index_col=0)
        logger.info("Predict result for new student")
    else: 
        raise ValueError("No predictive score")
    #data to train
    if args.data is not None:
        df = pd.read_csv(args.data, index_col=0)
    else:
        raise ValueError("No input data.")

    new_score = post_model(df, stud_to_pred, option, **config["post_model"])

     
    if args.output is not None:
        pd.DataFrame(np.array([new_score])).to_csv(args.output,index = False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Evaluate Model")
    parser.add_argument('--config', '-c', help='path to yaml file with configurations')
    parser.add_argument('--input', '-i', default=None, help="Path to CSV for input to model evaluation")
    parser.add_argument('--option','-op', default='GRE', help = "Choose a subject to predict.")
    parser.add_argument('--data', '-d', help = 'path to raw student dataset.')
    parser.add_argument('--output', '-o', default=None, help='Path to save the output file.')

    args = parser.parse_args()

    run_post_model(args)