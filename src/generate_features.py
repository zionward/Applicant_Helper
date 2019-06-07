import logging
import argparse
import yaml
import os
#import config
import pandas as pd
import numpy as np
# from load_data import download_from_s3

#logging.config.fileConfig(config.LOGGING_CONFIG)
logger = logging.getLogger(__name__)


def reset_y(df, cutoff = 0.7):
    """Reset the predictive value to 0 or 1 based on given cut-off
    Args:
    df (:py:class:`pandas.DataFrame`): A pandas dataframe.
    cutoff (float): Optional. A float number between 0 and 1 to set the percentage of training data.

    Returns:
    df_logit (:py:class:`pandas.DataFrame`): A pandas dataframe with updated result column
    """
    logger.debug("Reset response...")
    if cutoff < 0 or cutoff > 1:
        raise ValueError("cutoff should be float between 0 and 1.")
    
    df_logit = df
    df_logit = df_logit.rename(columns = {'Chance of Admit':'result'})
    df_logit = df_logit.rename(columns = {'GRE Score':'GRE'})
    df_logit = df_logit.rename(columns = {'TOEFL Score':'TOEFL'})
    df_logit = df_logit.rename(columns = {'University Rating':'University_rating'})
    df_logit.result[df_logit.result < cutoff] = 0
    df_logit.result[df_logit.result >= cutoff] = 1

    return df_logit

def get_features(df, selected_columns = None, target = None, save_path = None, **kwargs):
    """Selected specified columns or/and target from dataset if specified.
    Args:
        df (:py:class:`pandas.DataFrame`): A pandas dataframe.
        selected_columns (list): Optional. A list of columns which will be extract from df. Default is None.
        target (str): Optional. a string which is one column of the dataset and will be treated as target value in predictive model.
        save_path (str): Optional. Path to save the selected features. Default is None.
    
    Returns:
    X (:py:class:`pandas.DataFrame`): A pandas dataframe with selected features.
    """
    logger.debug("Select features...")
    if selected_columns is not None:
        features = [] # columns that will be kept
        drops = [] # columns that will be dropped
        for col in df.columns:
            if col in selected_columns or col.split("_dummy_")[0] in selected_columns or col == target:
                features.append(col)
            else:
                drops.append(col)
    #drop columns
        if len(drops) > 0:
            logger.info("The following columns will be dropped: %s" % ",".join(drops))
        
        logger.debug(features)
        X = df[features]
    #No selected column
    else:
        logger.debug("No feature selected. Will return original dataframe.")
        X = df

    if save_path is not None:
        X.to_csv(save_path)
    
    return X

def get_target(df, target, save_path = None, **kwargs):
    """Get a predicted result based on given columns
    Args:
        df (:py:class:`pandas.DataFrame`): A pandas dataframe.
        target (str): A column name selected as target.
        save_path: Optional. Path to save the target column. Default is None.
    Returns:
        y (:py:class:`pandas.DataFrame`): A pandas dataframe which is the target column.
    """

    y = df[target]

    if save_path is not None:
        y.to_csv(save_path, **kwargs)

    return y.values



def generate_features(df, save_path=None, **kwargs):
    """Generate more possible features including visible_range, visible_norm_range,
     log_entropy, entropy_x_contrast, IR_range and IR_norm_range
    Args:
        df (:py:class:`pandas.DataFrame`): A pandas dataframe.
        save_path: Optional. Path to save the generated features. Default is None.
        **kwargs: datafram with selected features that will be transformed.
    Returns:
        df (:py:class:`pandas.DataFrame`): A pandas dataframe with new generated features.
    """
    
    #Get datafram with selected features that will be transformed
    selected_columns_kwards = get_features(df, **kwargs["get_features"])
    df = get_features(df, selected_columns_kwards)
    df_reset = reset_y(df, **kwargs["reset_y"])
    print("cur_df", df.head())


    if save_path is not None:
        df_reset.to_csv(save_path)

    return df_reset


def run_generate_features(args):
    """Excute generate_features function with given config
    Args: From argparse, should contain args.config and optionally contains the save_path
        args.config (str): Path to yaml file
        args.input (str): Optional. Path to Input dataframe.
        args.output (str): Optional. Path to Output dataframe.
    Returns: 
        None
    """

    with open(args.config, "r") as f:
        config = yaml.load(f)

    if args.input is not None:
        df = pd.read_csv(args.input)
    #elif "load_data" in config:
        #df = download_from_s3(args)
    else:
        raise ValueError("No input data. Nor with path to dataframe nor config with load_data")
    
    df = generate_features(df, **config["generate_features"])

    if args.output is not None:
        df.to_csv(args.output)
        
    return df

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "Generate features")
    parser.add_argument('--config', help = "Path to yaml file with config information")
    parser.add_argument('--input', help = "Path to input dataframe")
    #parser.add_argument('--output', help = "Path to output dataframe")
    parser.add_argument("--bucket_name", help = "s3 bucket name")
    parser.add_argument("--file_key", help = "Name of the file in S3 that you want to download")
    parser.add_argument("--output_file_path", help = "output path for downloaded file")
    parser.add_argument("--output", help = "output path for output file") 
    args = parser.parse_args()

    run_generate_features(args)