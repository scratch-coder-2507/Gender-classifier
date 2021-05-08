from flask import Flask, render_template, url_for,request
from flask_bootstrap import Bootstrap
import pandas as pd
import numpy as np

#ML pacjages
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.externals import joblib

app = Flask(__name__)
Bootstrap(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict',methods=['POST'])
def predict():
	df = pd.read_csv("data/names_dataset.csv")
	#features and labels
	df_X = df.name
	df_Y = df.sex

	#Vectorization
	corpus = df_X
	cv = CountVectorizer()
	X = cv.fit_transform(corpus)

	#Loading our ML model
	naivebayes_model = open("models/naivebayesgendermodel.pkl","rb")
	clf = joblib.load(naivebayes_model)

	#Receives the input query from form
	if request.method=='POST':
		namequery = request.form['namequery']
		data = [namequery]
		vect = cv.transform(data).toarray()
		myprediction = clf.predict(vect)
	return render_template('results.html',prediction = myprediction,name = namequery.upper())




if __name__ == '__main__':
    app.run(debug=True)


