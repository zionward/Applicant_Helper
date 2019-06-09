import logging
import argparse
import yaml
import os
import subprocess
import pickle

import sklearn
import pandas as pd
import numpy as np

# from load_data import load_data
from src.generate_features import get_features, get_target
from src.train_model import train_test_split
from sklearn.linear_model import LogisticRegression

logger = logging.getLogger(__name__)
score_model_kwargs = ["predict"]

def test_model(X_test, model_path, save_score, **kwargs):
    """ Calculate the socre for the predictive model.
    Args:
        X_test: (:py:class:`pandas.DataFrame`): a pandas dataframe containing testing dataset
        model_path (str): the path to the logistic regression model
        save_score (str): Optional. The path to save the score
    Returns:
        y_pred_df (:py:class:`pandas.DataFrame`): a pandas dataframe, containing predicted class of testing data.
    """

    #get predictors
    with open(model_path, "rb") as f:
        logreg = pickle.load(f)
    
    #predict
    y_pred = logreg.predict(X_test)
    if save_score is not None:
        y_pred_df = pd.DataFrame(y_pred)
        y_pred_df.columns = ['result']
        y_pred_df.to_csv(save_score, index = False)

    return y_pred_df

def run_test_model(args):
    """Execute score_model based on given configuration
    Args:
    args: From argparse, should contain args.config and optionally contain args.save
        args.config (str): Path to yaml file with score_model
        args.input(str): Optional. Path to input dataframe.
        args.output(str): Optional. Path to output dataframe.
    Returns:
        None
    """

    with open(args.config, "r") as f:
        config = yaml.load(f)

    if args.input is not None:
        X_test = pd.read_csv(args.input, index_col = 0)
    else:
        raise ValueError("No input data.")

    y_predicted = test_model(X_test, **config["test_model"]) 

    if args.output is not None: 
        y_pred_df = pd.DataFrame(y_predicted)
        y_pred_df.columns = ['result']
        y_pred_df.to_csv(args.output, index = False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Score model")
    parser.add_argument('--config', '-c', help='path to yaml file with configurations')
    parser.add_argument('--input', '-i', default=None, help="Path to input dataframe")
    parser.add_argument('--output', '-o', default=None, help='Path to output file')
    args = parser.parse_args()

    run_test_model(args)



