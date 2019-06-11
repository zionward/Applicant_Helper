# Project Outline

<!-- toc -->

- [Project Charter](#project-charter)
- [Project Planning](#project-planning)
- [Repo structure](#repo-structure)
- [Documentation](#documentation)
- [Running the application](#running-the-application)
  * [1. Set up environment](#1-set-up-environment)
    + [With `virtualenv` and `pip`](#with-virtualenv-and-pip)
    + [With `conda`](#with-conda)
  * [2. Configure Flask app](#2-configure-flask-app)
  * [3. Initialize the database](#3-initialize-the-database)
  * [4. Run the application](#4-run-the-application)
- [Testing](#testing)

<!-- tocstop -->

## Project Charter 

**Vision**

Evaluate if a student can be admitted by the master program, and help them know how much they have to improve in a specific area in order to have a larger probability to be admitted.

**Mission**
 - By analyzing the admitted students’ common advantages, conclude the importance for each part of students' application.
 - Estimate the probability of a student to be admitted by the master program based on the input information using classification model.
 - Help student know how much they need to improve in a specific area (like how much score they need to improve in TOFEL) using established model and binary search.

**Success Criteria**
 - Machine Learning Performance metric: The confusion matrix will be used to measure the performance of the model. The success criteria for the classification model is prediction accuracy over 80%, and the precision is expected over 0.8 and the recall over 0.7.
 - Business outcome metric: Check if this app will increase the admission rate for perspective students.

## Project Planning 

**Main Theme**

There might be different weights for different parts of the students' application. To have a view of how much these different scores weight for the admission result, student can allocate their time and efforts on each exam better. Also, students might have different background in their application process. It will be helpful for them to track if they could be admitted based on their current score. They might also need to see how much they have to improve one area if they still have time to take actions. 

**Epic 1**: There are various types of student with different backgrounds. For example, some of them spend more time on researches, some of them focus more on the coursework. This app will display the ordinary criteria for each object in application for the reference of prospective students.
 - Story 1:  Go through the overall dataset and perform summary analysis to see if the data is biased in a specific aspect;.
 - Story 2: Compare students who were admitted by the master program and those were not. Conclude the common properties for those admitted student using clustering. 
 - Story 3: Visualize those different types of admitted student to help users have a better view. 


**Epic 2**: Students want to know if they will be admitted based on their current status in some certain confidence level. 

 - Story 1: Update the predicted value based on the imputed confidence interval, and set up the interactive function. 
 - Story 2: Model this classification problem using all features. As the new student’s information entered, the app will give an estimation of whether this student could be admitted based on current status. 
 - Story 3: Some student might do not take some exam, and it might be not fair for count it as 0. It would be helpful to select the objects that students have for prediction.
 - Story 4: Add some exogenous factors that may have an influence on student’s admission probability, but student cannot control/change. For example, some schools prefer to admit students whose parent is an alumna/alumnus; some schoomay have certain proportion of students from a specific country etc. This requires a larger data set about students’ bio-info and involves more heterogeneities.



**Epic 3**: Students who get an estimated result of not being admitted might want to improve a specific area to increase the probability to be admitted. For example, a student might have another chance to take a TOFEL or GRE, and he or she would want to know how much score they need to get in these two exams, and choose the one that is relatively easier to achieve. This app will give a minimum improved score in a specific area for a student to be estimated as “admitted”.

 - Story 1: Use the previous model and binary search (or other optimization method) to estimate the minimum score that they need to improve in this part in order to be admitted by the master program. 
 - Story 2: Make an interactive function that users can select the part they would like to improve. 
 - Story 3: Add the function that allows students to choose a cutoff line for being estimated as "admitted". 

**Epic 4** This model would be deployed onto AWS in the form of web app.

 - Story 1: Transfer the project from local to AWS. 
 - Story 2: Design the user interface to make it easy to achieve user interaction.

### Backlog 

1. epic1.story1: Data Cleaning and EDA (2 point) -- Planned
2. epic1.story2: Clustering (4 point) -- Planned
3. epic1.story3: Visualization (2 point) -- Planned
4. epic2.story1: Predictive Model Data Preparation (2 point)
5. epic2.story2: Model (Prediction) Building and Evaluation (8 point)
6. epic3.story1: Model (Binary Search) Building (8 point)
7. epic3.story2: Application of the binary search model to different objects (4 point)
8. epic3.story3:  Adding customized cutoff (2 point)
### IceBox 
1. epic2.story3: Objects Selection (4 points)
2. epic2.story4: Exogenous Factors Exploration （8 points）
3. epic4.story1: Transition from local to AWS (8 points)
4. epic4.story1: App Development (8 point)


## Repo structure 

```
├── README.md                         <- You are here
│
├── app
│   ├── static/                       <- CSS, JS files that remain static 
│   ├── templates/                    <- HTML (or other code) that is templated and changes based on a set of inputs
│   ├── __init__.py                   <- Initializes the Flask app and database connection
│
├── config                            <- Directory for yaml configuration files for model training, scoring, etc
│   ├── logging/                      <- Configuration files for python loggers
│
├── data                              <- Folder that contains data used or generated. Only the external/ and sample/ subdirectories are tracked by git. 
│
├── docs                              <- A default Sphinx project; see sphinx-doc.org for details.
│
├── models                            <- Trained model objects (TMOs), model predictions, and/or model summaries
│
├── notebooks
│   ├── develop                       <- Current notebooks being used in development.
│   ├── deliver                       <- Notebooks shared with others. 
│   ├── archive                       <- Develop notebooks no longer being used.
│
├── src                               <- Source data for the project 
│   ├── helpers/                      <- Helper scripts used in main src files 
│   ├── sql/                          <- SQL source code
│   ├── load_data.py                  <- Script download admission dataset from public S3 busket
│   ├── generate_features.py          <- Script for cleaning and transforming data and generating features used for use in training and scoring.
│   ├── train_model.py                <- Script for training logistic regression for the admission result
│   ├── score_test_model.py                <- Script for scoring testing predictions using a trained model.
│   ├── eval_model.py             <- Script for evaluating model performance 
│   ├── socre_model.py                <- Script for predict one new student prediction result (like what )
│   ├── post_model.py                <- Script for search optimal score of specified subject to help student be admitted
│   ├── database_model.py                <- Script for creating database model that is later connect to the Flask APP
│
├── test                              <- Files necessary for running model tests (see documentation below) 
│   ├── test.py                <- unit test for code in /src

├── run.py                            <- Simplifies the execution of one or more of the src scripts 
├── app.py                            <- Flask wrapper for running the model 
├── config.py                         <- Configuration file for Flask app
├── requirements.txt                  <- Python package dependencies 
```
This project structure was partially influenced by the [Cookiecutter Data Science project](https://drivendata.github.io/cookiecutter-data-science/).

## Documentation
 
* Open up `docs/build/html/index.html` to see Sphinx documentation docs. 
* See `docs/README.md` for keeping docs up to date with additions to the repository.

## Instructions on getting data and database ready
* See `src/README.md` for guideline of setting dataset

## Running the application 
### 1. Set up environment 

The `requirements.txt` file contains the packages required to run the model code. An environment can be set up in two ways. 

First, `cd path_to_repo`

#### With `virtualenv`

```bash
pip install virtualenv

virtualenv pennylane

source pennylane/bin/activate

pip install -r requirements.txt

```
#### With `conda` （recommend）

```bash
conda create -n pennylane python=3.6
conda activate pennylane
pip install -r requirements.txt
```

### 2. Configure Flask app 

`config.py` holds the configurations for the Flask app. It includes the following configurations:

```python
DEBUG = True  # Keep True for debugging, change to False when moving to production 
LOGGING_CONFIG =  "config/logging/local.conf"  # Path to file that configures Python logger
PORT = 3000  # What port to expose app on 
SQLALCHEMY_DATABASE_URI = 'sqlite:///src/user_prediction.db'# URI for database that contains tracks
```

### 3. Initialize the database 

#### Locally

To create the database in the location configured in `config.py` with one initial student, run: 

`python src/database_model.py`

The database `students_prediction.db` will be created in current directory.

To add additional student information, run the web-app and  enter the student info will be recorded.

#### RDS

To create the database on RDS in the location configured in `config.py` with one initial bank customer, first change path to where the file is located and run:

`python src/database_model.py --RDS True`

To add additional student information, run the web-app and  enter the student info will be recorded.


### 4. Run the application 

#### Local
To run this app locally,  run following line to train model:
```bash
make all
```
After checking the evaluation (AUC and Confusion Matrix) in models file, if you feel this model looks good, then run the web-app using:
 ```bash
 python app.py 
 ```
### RDS
To run the application on RDS, unncomment following lines in `config.py`.
```bash
 SQLALCHEMY_DATABASE_URI =  'sqlite:///src/user_prediction.db'
 ```
 and add 
 ``` bash
 SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
conn_type = "mysql+pymysql"
user = os.environ.get("MYSQL_USER")
password = os.environ.get("MYSQL_PASSWORD")
host = os.environ.get("MYSQL_HOST")
port = os.environ.get("MYSQL_PORT")
DATABASE_NAME = 'msia423'
SQLALCHEMY_DATABASE_URI =SQLALCHEMY_DATABASE_URI.format(conn_type=conn_type, user=user, password=password, host=host, port=port, DATABASE_NAME=DATABASE_NAME)
 ```
 Also, change the current `HOST` from:
 ```bash
HOST =  "127.0.0.1"
```
to
```bash
HOST = "0.0.0.0"
```
Then run the model:
```bash
make all
```
then run the application:
```bash
python app.py
```

💡 Tips: If you meet the following error:
```bash
AttributeError: 'NoneType' object has no attribute 'format'
```
Please run following command in terminal before run `make all`:
```bash
export SQLALCHEMY_DATABASE_URI="{conn_type}://{user}:{password}@{host}:{port}/{DATABASE_NAME}"
```

💡If your get info when you run `make all`:
```bash
make: Nothing to be done for `all'.
```
that means the train-model part has been done. You can run `python app.py` directly. If you want to train-model again, please run the following command before you run `make all`:
```bash
make clean
```


### 5. Interact with the application 

Go to [http://127.0.0.1:3000/]( http://127.0.0.1:3000/) to interact with the current version of this web-app. 

## Testing 

Run `make test` from the command line in the main project repository. 

Tests exist in `test/test.py`
<!--stackedit_data:
eyJoaXN0b3J5IjpbMzY2OTgyOTZdfQ==
-->