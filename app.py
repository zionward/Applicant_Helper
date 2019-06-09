from flask import render_template, request, redirect, url_for
import logging.config
from app import db, app
from src.database_model import Student_Prediction
import traceback
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import pickle
from src.load_data import download_from_s3
# from src.generate_features import reset_y
import sklearn
from sklearn.linear_model import LogisticRegression
import math

# Define LOGGING_CONFIG in config.py - path to config file for setting up the logger (e.g. config/logging/local.conf)
logging.config.fileConfig(app.config["LOGGING_CONFIG"])
logger = logging.getLogger("penny-lane")
logger.debug('Test log')

#Initialize flask
app = Flask(__name__)
#add configuration of flask
app.config.from_object('config')

#initial database
db = SQLAlchemy(app)



@app.route('/')
def index():
    """Main view that lists songs in the database.

    Create view into index page that uses data queried from Track database and
    inserts it into the msiapp/templates/index.html template.

    Returns: rendered html template

    """

    try:
        #tracks = Track.query.all()
        logger.debug("Index page accessed")
        return render_template('index.html')
    except:
        logger.warning("Not able to display tracks, error page returned")
        return render_template('error.html')


@app.route('/add', methods=['POST','GET'])
def add_entry():
    """View that process a POST with new song input

    :return: redirect to index page
    """
    try:
        #retreve features
        logger.info("Getting user input")
        GRE = request.form['GRE']
        TOEFL = request.form['TOEFL']
        university_rating = request.form['University_Rating']
        SOP = request.form['SOP']
        LOR = request.form['LOR']
        CGPA = request.form['CGPA']
        research = request.form['research']
        logger.info('user inputs get')

        #load model
        path_to_data = app.config["DATA_PATH"]
        model_path = app.config["MODEL_PATH"]
        data = pd.read_csv(path_to_data)

        X = data[["GRE","TOEFL","University_rating", "SOP","LOR","CGPA","Research"]]
        y = data["result"]

        X_mean = X.mean()
        X_std = X.std()
        # X_mean = pd.DataFrame([list(X_mean.values)],columns=list(X_mean.index))
        # X_std = pd.DataFrame([list(X_std.values)],columns=list(X_std.index))
        X_mean.to_csv("models/coef_mean.csv")
        X_std.to_csv("models/coef_std.csv")
        
        with open(model_path, "rb") as f:
            logreg = pickle.load(f)
        print("The coefs of the model are as following: ", logreg.coef_)
        new_stud = pd.DataFrame(columns=["GRE","TOEFL","University_rating", "SOP","LOR","CGPA","Research"])
        new_stud.loc[0] = [GRE,TOEFL,university_rating, SOP,LOR,CGPA,research]        
        new_stud = new_stud.apply(pd.to_numeric)
        print("new_stud is ", new_stud)
        new_stud.to_csv("models/new_stud.csv", index = False)
        #predict result
        new_stud_nor= (new_stud - X_mean)/X_std
        y_new = logreg.predict(new_stud_nor)
        # print("The predit result is", y_new)
        result = y_new[0]

        if result == 0:
            return render_template('index_score.html', new_stud =new_stud, X_mean = X_mean, X_std = X_std, model = logreg)
        else:
            return render_template('index_congrats.html', new_stud =new_stud, X_mean = X_mean, X_std = X_std, model = logreg)
        #add track
        student = Student_Prediction(GRE=GRE, TOEFL=TOEFL, university_rating=university_rating,
                                       SOP = SOP, LOR = LOR, CGPA = CGPA, research = research)
        db.session.add(student)
        db.session.commit()
        #logger.info("New song added: %s by %s", request.form['title'], request.form['artist'])
        

    except:
        traceback.print_exc()
        logger.warning("Not able to display tracks, error page returned")
        return render_template('error.html')



@app.route('/bs', methods=['POST','GET'])
def predict_entry():

# #     """View that process a POST with new song input

# #     :return: redirect to index page
# #     """
    try:
        logger.info("Getting user input")
        model_path = app.config["MODEL_PATH"]
        option = int(request.form['subject'])
        with open(model_path, "rb") as f:
            logreg = pickle.load(f)
        X_mean = pd.read_csv("models/coef_mean.csv", header = None)
        idx = X_mean.iloc[:,0]
        X_mean= pd.Series(X_mean.iloc[:,1])
        X_mean.index = idx
        X_std = pd.read_csv("models/coef_std.csv",header = None)
        idx = X_std.iloc[:,0]
        X_std= pd.Series(X_std.iloc[:,1])
        X_std.index = idx
        new_stud = pd.read_csv("models/new_stud.csv")
        input_GRE = new_stud.iloc[0]['GRE']
        input_TOEFL = new_stud.iloc[0]['TOEFL']
        new_stud = (new_stud-X_mean)/X_std
        if option == 0:
            new_GRE = input_GRE
            new_stud2 =new_stud
            new_stud2["GRE"] = (340 - X_mean['GRE'])/X_std['GRE']
            y_new = logreg.predict(new_stud2)
            #Base case: check if full grade in this project can be admit
            if y_new[0] == 0: 
                high_score = "Cannot get admitted by improving only GRE. Fighting!"
                return render_template('index_score.html', high_score = high_score, result = "red")
            low_pred = 0
            low_score = new_GRE
            high_pred = y_new[0]
            high_score = 340
            diff = high_score - low_score
            while diff > 1:
                mid_score = low_score + math.floor(diff/2)
                new_stud2['GRE'] = (mid_score - X_mean['GRE'])/X_std['GRE']
                y_new = logreg.predict(new_stud2)
               # print("mid_score is ", mid_score)
               # print("current predictive result is", y_new[0])
                if y_new[0]*high_pred < 1:#mid is not admitted, go to upper part
                    low_score = mid_score
                else: #mid is admitted, go to lower part
                    high_score = mid_score
                diff = high_score - low_score
                
        else:
            new_TOEFL = input_TOEFL
            new_stud2 =new_stud
            new_stud2["TOEFL"] = (120 - X_mean["TOEFL"])/X_std["TOEFL"]
            y_new = logreg.predict(new_stud2)
            #cur_score = stud_to_pred["TOEFL"][0]
            #Base case: check if full grade in this project can be admit
            if y_new[0] == 0: 
                high_score = "Cannot get admitted by improving only TOEFL. Fighting!"
                return render_template('index_score.html', high_score = high_score, result = "red")
            low_pred = 0
            low_score = new_TOEFL
            high_pred = y_new[0]
            high_score = 120
            diff = high_score - low_score
            while diff > 1:
                mid_score = low_score + math.floor(diff/2)
                stud_to_pred2['TOEFL']= (mid_score - X_mean["TOEFL"])/X_std["TOEFL"]
                y_new = logreg.predict(new_stud2)
                if y_new[0]*high_pred < 1:#mid is not admitted, go to upper part
                    low_score = mid_score
                else: #mid is admitted, go to lower part
                    high_score = mid_score
                diff = high_score - low_score

        high_score = "The minimum score that can help you to be admitted is " + str(high_score)
        return render_template('index_score.html', high_score = high_score, result = "green")
    except:
        traceback.print_exc()
        logger.warning("Not able to display tracks, error page returned")
        return render_template('error.html')


if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"], port=app.config["PORT"], host=app.config["HOST"])

