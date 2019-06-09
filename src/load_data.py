import sys
import os
import json
import logging
import requests
import numpy as np
import pandas as pd
import yaml
import argparse
import boto3
import botocore

logger = logging.getLogger(__name__)

s3 = boto3.client("s3", config=botocore.client.Config(signature_version=botocore.UNSIGNED))


def download_from_s3(args):
    s3.download_file(args.bucket_name, args.file_key, args.output_file_path)
    


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "")
    parser.add_argument("--config", help = "Path to .yaml file with config.")
    parser.add_argument("--bucket_name", help = "s3 bucket name")
    parser.add_argument("--file_key", help = "Name of the file in S3 that you want to download")
    parser.add_argument("--output_file_path", help = "output path for downloaded file")
    #parser.add_argument("--save", default = None, help = "Path to save the output dataframe. Default is None.")

    args = parser.parse_args()
    #print(args.config, args.bucket_name)

    download_from_s3(args)
