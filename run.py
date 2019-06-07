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
logging.config.fileConfig("config/logging/local.conf")
logger = logging.getLogger("run-penny-lane")

from src.generate_features import run_generate_features
from src.train_model import run_train_model
from src.score_model import run_score_model
from src.post_model import run_post_model



if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Run components of the model source code")
    subparsers = parser.add_subparsers()

    # Generate Features
    sb_features = subparsers.add_parser("generate_features", description = "Generate features")
    sb_features.add_argument('--config', help = "Path to yaml file with config information")
    sb_features.add_argument('--input', help = "Path to input dataframe")
    sb_features.add_argument("--bucket_name", help = "s3 bucket name")
    sb_features.add_argument("--file_key", help = "Name of the file in S3 that you want to download")
    sb_features.add_argument("--output_file_path", help = "output path for downloaded file")
    sb_features.add_argument("--output", help = "output path for output file") 
    sb_features.set_defaults(func=run_generate_features)

    # Sub-parser for building model for database student 
    sb_model = subparsers.add_parser("train_model", description="train model")
    sb_model.add_argument('--config', default="config.yaml",
                        help='path to yaml file with configurations')
    sb_model.add_argument('--input', default=None, help="Path to input dataframe")
    sb_model.add_argument('--output', default=None, help='Path to output dataframe')
    sb_model.set_defaults(func=run_train_model)

    #sub-parser for predicting new studenn
    sb_score = subparsers.add_parser("score_model", description="predict new student application result")
    sb_score.add_argument('--config', '-c', help='path to yaml file with configurations')
    sb_score.add_argument('--input', '-i', default=None, help="Path to input dataframe")
    sb_score.add_argument('--output', '-o', default=None, help='Path to output file')
    sb_score.set_defaults(func=run_score_model)

    #sub-parser for predicting optimal score
    sb_post = subparsers.add_parser("post_model", description="predict minimum score of selected subjesct to help a student be admitted")
    sb_post.add_argument('--config', '-c', help='path to yaml file with configurations')
    sb_post.add_argument('--input', '-i', default=None, help="Path to CSV for input to model evaluation")
    sb_post.add_argument('--option','-op', default='GRE', help = "Choose a subject to predict.")
    sb_postparser.add_argument('--data', '-d', help = 'path to raw student dataset.')
    sb_post.add_argument('--output', '-o', default=None, help='Path to save the output file.')
    sb_post.set_defaults(func=run_post_model)


    args = parser.parse_args()
    args.func(args)