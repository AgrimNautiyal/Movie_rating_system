from flask import Flask, render_template, request
from wtforms import Form, TextAreaField, validators
import sqlite3
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import os
import numpy as np


app = Flask(__name__)


@app.route('/')
def index():
	return render_template('LandingPage.html')


#TO SIGNUP
@app.route('/sign_up', methods = ['GET', 'POST'])
def signup():
       return render_template('sign_up.html')

@app.route('/signup_input', methods = ['GET', 'POST'])
def signupinput():
        username = request.form['UserName']
        password = request.form['Password']
        with sqlite3.connect('softwareproject.db') as con:
                cur = con.cursor()
                cur.execute('''INSERT INTO User_Auth VALUES(?,?)''',(username, password))
                
        return render_template('signupconf.html')

#TO LOGIN
@app.route('/login', methods = ['GET','POST'])
def loginpagerender():
        return render_template('login.html')

@app.route('/login_input',methods = ['GET','POST'] )
def logincheck():
        username = request.form['UserName']
        password = request.form['Password']
        print(username)
        print(password)

        with sqlite3.connect('softwareproject.db') as con:
                cur = con.cursor()
                cur.execute('SELECT Password from User_Auth where UserId =?''',(username,))
                correct_pass = cur.fetchall()
        if(correct_pass[0][0] == password):
                return render_template('successfullogin.html')
        else:
                return render_template('unsuccessfulloginattempt.html')

#TO PLAY AROUND WITH MOVIE RATING WITHOUT LOGIN
@app.route('/results', methods=['POST'])
def predict():
        sentence = str(request.form['review'])
        sid = SentimentIntensityAnalyzer()
        ss = sid.polarity_scores(sentence)

        if ss['compound']<0:
                score = 10-abs((ss['compound']*10))+0.5
        else:
                score = (ss['compound']*10)-0.5
	
        return render_template('results.html', res=score)

if __name__ == '__main__':
	app.run(debug=True)
