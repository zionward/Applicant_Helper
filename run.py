"""Enables the command line execution of multiple modules within src/

This module combines the argparsing of each module within src/ and enables the execution of the corresponding scripts
so that all module imports can be absolute with respect to the main project directory.

Current commands enabled:

To create a database for Tracks with an initial song:

    `python run.py create --artist="Britney Spears" --title="Radar" --album="Circus"`

To add a song to an already created database:

    `python run.py ingest --artist="Britney Spears" --title="Radar" --album="Circus"`
"""
import argparse
import logging.config
from app import app
import logging.config
# logging.config.fileConfig("config/logging/local.conf")
# logger = logging.getLogger("run-penny-lane")


# Define LOGGING_CONFIG in config.py - path to config file for setting up the logger (e.g. config/logging/local.conf)
logging.config.fileConfig(app.config["LOGGING_CONFIG"])
logger = logging.getLogger("applicant-helper")
logger.debug('Test Log')


from src.generate_features import run_generate_features
from src.train_model import run_train_model
from src.score_test_model import run_test_model
from src.post_model import run_post_model
from src.eval_model import run_evaluate_model



if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Run components of the model source code")
    subparsers = parser.add_subparsers()


    
    # Generate Features
    sb_features = subparsers.add_parser("generate_features", description = "Generate features")
    sb_features.add_argument('--config', help = "Path to yaml file with config information")
    sb_features.add_argument('--input', help = "Path to input dataframe")
    sb_features.add_argument("--output", help = "output path for output file") 
    sb_features.set_defaults(func=run_generate_features)

    # Train Model
    sb_model = subparsers.add_parser("train_model", description="train model")
    sb_model.add_argument('--config', default="config.yaml",
                        help='path to yaml file with configurations')
    sb_model.add_argument('--input', default=None, help="Path to input dataframe")
    sb_model.add_argument('--output', default=None, help='Path to output dataframe')
    sb_model.set_defaults(func=run_train_model)

    #sub-parser for predicting new studenn
    sb_score = subparsers.add_parser("score_test_model", description="predict testing student application result")
    sb_score.add_argument('--config', '-c', help='path to yaml file with configurations')
    sb_score.add_argument('--input', '-i', default=None, help="Path to input dataframe")
    sb_score.add_argument('--output', '-o', default=None, help='Path to output file')
    sb_score.set_defaults(func=run_test_model)

    #sub-parser for predicting optimal score
    sb_eval = subparsers.add_parser("run_evaluate_model", description="predict minimum score of selected subjesct to help a student be admitted")
    sb_eval.add_argument('--config', '-c', help='path to yaml file with configurations')
    sb_eval.add_argument('--Xtest', '-x', default=None, help="Path to CSV for features to model evaluation")
    sb_eval.add_argument('--input', '-i', default=None, help="Path to CSV for input to model evaluation")
    sb_eval.add_argument('--output', '-o', default=None, help='Path to save the output file.')
    sb_eval.set_defaults(func=run_evaluate_model)


    args = parser.parse_args()
    args.func(args)