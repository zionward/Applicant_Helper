import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import seaborn as sns
import sys
import os

import argparse
import logging
import yaml
import pickle
import sklearn
from sklearn.linear_model import LogisticRegression
from src.generate_features import get_features, get_target


logger = logging.getLogger(__name__)
methods = dict(logistic=LogisticRegression)

def get_mean(df,**kwargs):
    """Get column mean of features of dataframe
    Args:
    df (:py:class:`pandas.DataFrame`): A pandas dataframe.
    
    Returns:
    X.mean (:py:class:`pandas.DataFrame`): A one line pandas dataframe with mean of each feature.
    """ 
    logger.debug("Get Mean...")
    return df.mean()


def get_sd(df,**kwargs):
    """Get column standard deviation of features of dataframe
    Args:
    df (:py:class:`pandas.DataFrame`): A pandas dataframe.
    
    Returns:
    X.std (:py:class:`pandas.DataFrame`): A one line pandas dataframe with mean of each feature.
    """
    logger.debug("Get Standard Deviation...")
    return df.std()

def normalize_features(X, save_path = None, **kwargs):
    """Noemalize specified columns or/and target from dataset if specified.
    Args:
        X (:py:class:`pandas.DataFrame`): A pandas dataframe.
        save_path (str): Optional. Path to save the selected features. Default is None.
    
    Returns:
    df_X (:py:class:`pandas.DataFrame`): A pandas dataframe with normalized features.
    
    """

    logger.debug("normalize features...")

    mean_X = get_mean(X)
    std_X = get_sd(X)
    df_X =  (X - mean_X)/std_X
    
    return df_X
    

def train_test_split(X, y, train_ratio = 0.8, test_ratio = 0.2, random_seed = 42, save_split = None):
    """Split the data with give train/test ratio.

    Args:
        X (:py:class:`pandas.DataFrame`): A pandas dataframe with predictors.
        y (:py:class:`pandas.DataFrame`): A pandas dataframe with predicted value.
        train_ratio (float): Optional. Fraction of train size. Default is 0.7.
        test_ratio (float): Optional. Fraction of test size. Default is 0.3.
        random_seed (int): Optional. Random seed. Default is 42.
        save_split (str): Optional. Path to save the splited dataframe. Default is None.
    Return:
        X (dict): A dictionary whose key is train, test and values are predictors dataframe of train data and test data.
        y (dict): A dictionary whose key is train, test and values are predicted value dataframe of train data and test data.
    """

    if train_ratio + test_ratio == 1:
        prop = True
    elif train_ratio + test_ratio == len(X):
        prop = False
    else:
        raise ValueError("train_size + test_size should equal to 1.")

    if prop:
        train_size = int(np.round(train_ratio*len(X)))
        test_size = int(len(X) - train_size)
    if train_size == 1:
        X_train, y_train = X,y
        X_test, y_test = [],[]
    elif test_size == 1:
        X_train, y_train = [],[]
        X_test, y_test = X,y
    else:
        X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(
            X, y, train_size=train_size, test_size=test_size, random_state=random_seed)
   
    X = dict(train=X_train)
    y = dict(train=y_train)

    if len(X_test) > 0:
        X["test"] = X_test
        y["test"] = y_test
        
    if save_split is not None:
        for split in X:
            pd.DataFrame(X[split]).to_csv("%s-%s-features.csv" % (save_split, split))
            pd.DataFrame(y[split]).to_csv("%s-%s-targets.csv"%(save_split, split))

            logger.info("Trin-Test split complete. X_%s and y_%s saved in %s-%s-features.csv and %s-%s-targets.csv", split, split, save_split, split, save_split,split)

    return X,y


def train_model(df, method = None, save_model = None, **kwargs):
    """Train a (logistic regression) model as specified.
    Args:
    df: (:py:class:`pandas.DataFrame` or :py:class:`numpy.Array`): A pandas dataframe
    method (list): methods for training, here is logistic regression
    ave_path (str): Optional. Path to save the trained logistic model. Default is None.
    
    Returns:
        model (pickle): a (logistic regression) model
    """
    #Assum method defined, in this case, logistic regression
    assert method in methods.keys()
    
    #get predictors from get_features method
    if "get_features" in kwargs:
        X = get_features(df, **kwargs["get_features"])
    else:
        X = df
    
    X = normalize_features(X)

    #get predicted value from get_target method
    if "get_target" in kwargs:
        y = get_target(df, **kwargs["get_target"])
        df = df.drop(labels = [kwargs["get_target"]["target"]],axis = 1)
    else:
        y = None

    #Split train set and test set

    X,y = train_test_split(X, y, **kwargs["train_test_split"])

    #Specified the method. In this case, logistic regression.
    model = methods[method]()

    #Fit model

    model.fit(X["train"], y["train"])

    #Save model if specified
    if save_model is not None:
        with open(save_model, "wb" ) as f: #write and binary
            pickle.dump(model,f)
        logger.info("Trained model save to %s", save_model)
    return model

def run_train_model(args):
    """Execute train_model with given config.
    Args: From argparse, should contain args.config and optionally contain arg.save
        args.config(str): Path to yaml file with train_model.
        args.input(str): Optional. Path to input dataframe.
        args.output(str): Optional. Path to output dataframe.
    Returns:
        None
    """

    with open(args.config, "r") as f:
        config = yaml.load(f)

    if args.input is not None:
        df = pd.read_csv(args.input)
    else:
        raise ValueError("Path to dataframe is not given.")

    model = train_model(df, **config["train_model"])

    if args.output is not None:
        with open(args.output, "wb") as f:
            pickle.dump(model,f)
        logger.info("Trained model save to %s" % args.output)


    