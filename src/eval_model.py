import logging
import argparse
import yaml
import os
import subprocess
import math
import seaborn as sns
import sys
import os

from sklearn import metrics

import pickle

import sklearn
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, recall_score, roc_auc_score, confusion_matrix, f1_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve
from sklearn.linear_model import LogisticRegression

import matplotlib.pyplot as plt
from src.generate_features import get_features, get_target
from src.train_model import train_test_split

logger = logging.getLogger(__name__)

def evaluate_model(df_score,X_test,model_path, save_eval = None, **kwargs):
    """Calculate the auc and accuracy for predictive model
    Args:
        df_score (:py:class:`pandas.DataFrame`): a pandas Dataframe containing the predictive score.
        X_test (:py:class:`pandas.DataFrame`): a pandas Dataframe containing the features of testing dataset.
        save_path (str): Optional. Path to save the output.

    Returns:
        metric (:py:class:`pandas.DataFrame`): a pandas dataframe containing AUC and Accuracy on test.
    """
    logger.debug("Evaluating models")

    #load model
    with open(model_path, "rb") as f:
        logreg = pickle.load(f)

    # get the predicted result 
    y_pred = df_score['result']

    # get the y_test from the csv of test_split data we split earlier
    y_test = pd.read_csv(kwargs["path_to_test_target"])['0']
    
    # compute the auc and accuracy scores and put them into a dataframe 
    confusion_mtx = confusion_matrix(y_test, y_pred)
    class_names=[0,1] # name  of classes
    fig, ax = plt.subplots()
    tick_marks = np.arange(len(class_names))
    plt.xticks(tick_marks, class_names)
    plt.yticks(tick_marks, class_names)
    # create heatmap
    sns_plot = sns.heatmap(pd.DataFrame(confusion_mtx), annot=True, cmap="YlGnBu" ,fmt='g')
    ax.xaxis.set_label_position("top")
    plt.tight_layout()
    plt.title('Confusion matrix', y=1.1)
    plt.ylabel('Actual label')
    plt.xlabel('Predicted label')
    fig = sns_plot.get_figure()
    fig.savefig("models/confusion_matrix")


    #Create AUC curve
    logit_roc_auc = roc_auc_score(y_test, logreg.predict(X_test))
    fpr, tpr, thresholds = roc_curve(y_test, logreg.predict_proba(X_test)[:,1])
    plt.figure()
    plt.plot(fpr, tpr, label='Logistic Regression (area = %0.2f)' % logit_roc_auc)
    plt.plot([0, 1], [0, 1],'r--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver operating characteristic')
    plt.legend(loc="lower right")
    plt.savefig('models/Log_ROC')

    auc = sklearn.metrics.roc_auc_score(y_test, y_pred)
    accuracy = sklearn.metrics.accuracy_score(y_test, y_pred)
    metric = pd.DataFrame({'auc':[auc],'accuracy': [accuracy]})

    # save the new dataframe of scores if necessary to the specified path 
    if save_eval is not None:
       metric.to_csv(save_eval, index=False)

    return metric

def run_evaluate_model(args):
    """Executes model evaluation based on given configuration.
    Args:
        args: From argparse, should contain args.config and optionally, args.save
            args.config (str): Path to yaml file with evaluate_model
            args.input (str): Optional. Path to input socre file
            args.Xtest (str): Optional. Path to testing dataset feature file
            args.output (str): Optional. Path to save the output result.
    Returns: None
    """
    with open(args.config, "r") as f:
        config = yaml.load(f)

    if args.input is not None:
        df = pd.read_csv(args.input)
        logger.info("Response for input into model loaded from %s", args.input)
    else:
        raise ValueError("No input data.")

    if args.Xtest is not None:
        X_test = pd.read_csv(args.Xtest,index_col=0)
        logger.info("Features for input into model loaded from %s", args.Xtest)
    else:
        raise ValueError("No input features")
        
    metric = evaluate_model(df,X_test, **config["evaluate_model"])


    
