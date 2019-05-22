# Guideline for running 

Here are three files that my QA needs to look at:

1. src/downloadFromS3.py: Download data from S3 to local path.
parameters that need to be specified when run this file:
--file_key: Name of the file in S3 that you want to download. In this case, enter "Admission_Predict.csv";
--bucket_name: s3 bucket name. In this case, enter "123sasa";
--output_file_path: output path for downloaded file.

2. src/uploadToS3.py: Upload local data to S3 bucket.
parameters that need to be specified when run this file:
--input_file_path: local path for uploaded file. In this case, enter "src/data/Admission_Predict.csv"
--bucket_name: s3 bucket name.
--output_file_path: output path for uploaded file

3. src/sql/database_model.py: Create database.
parameters that need to be specified when run this file:
--RDS: True if want to create in RDS else None. To check if work on RDS, please enter "True".

Note: Created database can be checked in the "src/sql/logfile"
