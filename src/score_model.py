import logging
import argparse
import yaml
import os
import subprocess
import pickle

import sklearn
import pandas as pd
import numpy as np

#from load_data import load_data
from generate_features import get_features, get_target
from train_model import train_test_split, get_mean, get_sd,normalize_features
from sklearn.linear_model import LogisticRegression

logger = logging.getLogger(__name__)

score_model_kwargs = ["predict"]

def get_new_student(new_student_df, new_CGPA, new_GRE, new_LOR, new_Research, new_SOP, new_TOEFL, new_University_rating, save_new_student):
    new_student_df = new_student_df.iloc[3:4]
    new_student_df.CGPA = new_CGPA
    new_student_df.GRE = new_GRE
    new_student_df.LOR = new_LOR
    new_student_df.Research = new_Research
    new_student_df.SOP = new_SOP
    new_student_df.TOEFL = new_TOEFL
    new_student_df.University_rating = new_University_rating
    #new_student_df = (new_student_df - X_mean)/X_std
    new_student_df.to_csv(save_new_student)
    return new_student_df

def normalize_new_student(new_student,df_mean, df_sd):
    return (new_student-df_mean)/df_sd

def score_model(new_student_df, model_path, save_score, **kwargs):
    """ Calculate the socre for new student.
    Args:
        df: (:py:class:`pandas.DataFrame`): a pandas dataframe 
        model_path (str): the path to the logistic regression model
        save_score (str): Optional. The path to save the score
    Returns:
        y_predicted (:py:class:`pandas.DataFrame`): a pandas dataframe, containing one predicted class and its corresponding probablity.
    """
    #Get predictors
    with open(model_path, "rb") as f:
        logreg = pickle.load(f)

    if "get_features" in kwargs:
        X = get_features(new_student_df,**kwargs["get_features"])
    else:
        X = new_student_df
    df_mean = get_mean(X)
    df_sd = get_sd(X)
    new_student = get_new_student(X, **kwargs["get_new_student"])
    new_student = normalize_new_student(new_student, df_mean, df_sd)
    y_new = logreg.predict(new_student)
    y_pred = y_new[0]

    if y_pred == 0:
        print("Sorry. You are not admitted.")
    else:
        print("Congrats! You are admitted!")

    if save_score is not None: 
        pd.DataFrame(y_new).to_csv(save_score, index = False)

    return y_new


def run_score_model(args):
    """Execute score_model based on given configuration
    Args:
    args: From argparse, should contain args.config and optionally contain args.save
        args.config (str): Path to yaml file with score_model
        args.input(str): Optional. Path to input dataframe.
        args.output(str): Optional. Path to output dataframe.
    Returns:
        None
    """

    with open(args.config,"r") as f:
        config = yaml.load(f)

    if args.input is not None:
        df = pd.read_csv(args.input)
    else:
        raise ValueError("No input data.")

    y_predicted = score_model(df, **config["score_model"])
    if args.output is not None:
        pd.DataFrame(y_predicted).to_csv(args.output, index = False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Score model")
    parser.add_argument('--config', '-c', help='path to yaml file with configurations')
    parser.add_argument('--input', '-i', default=None, help="Path to input dataframe")
    parser.add_argument('--output', '-o', default=None, help='Path to output file')

    args = parser.parse_args()

    run_score_model(args)