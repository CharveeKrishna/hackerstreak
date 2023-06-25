import requests
from isodate import parse_duration
from flask import *
from flask import render_template, current_app, request, redirect
from database import WorkspaceData
import pyrebase
import numpy as np
import pickle
from flask import Flask, redirect, url_for, render_template, request, jsonify, make_response
from chatbot2 import finalbot, sent_tokens


config = {
    "apiKey": "AIzaSyAtrTEGew0KD7b1NVDRKo4PlfbpC0-Xne4",
    "authDomain": "profiles-ecbb8.firebaseapp.com",
    "databaseURL": "https://profiles-ecbb8-default-rtdb.firebaseio.com",
    "projectId": "profiles-ecbb8",
    "storageBucket": "profiles-ecbb8.appspot.com",
    "messagingSenderId": "532219186559"
}

import os

YOUTUBE_API_KEY = os.environ.get('YOUTUBE_API_KEY')

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    return render_template("Home.html")


@app.route('/loginform', methods=['POST', 'GET'])
def loginform():
    return render_template('loginform.html')


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    return render_template('Page-1.html')


@app.route('/frontpage', methods=['POST', 'GET'])
def frontpage():
    return render_template('frontpage.html')

@app.route('/editprofile', methods=['POST', 'GET'])
def editprofile():
    return render_template('editprofile.html')



@app.route('/resume', methods=['POST', 'GET'])
def index():
    return render_template('index.html')


@app.route('/standardresume', methods=['POST', 'GET'])
def standardresume():
    return render_template('standardresume.html')


@app.route('/modrenresume', methods=['POST', 'GET'])
def modrenresume():
    return render_template('modrenresume.html')


@app.route('/compsearch', methods=['POST', 'GET'])
def compsearch():
    return render_template('compsearch.html', info_data=0)


@app.route('/visuallearning', methods=['POST', 'GET'])
def visuallearning():
    return render_template('visual-learning.html', info_data=0)


@app.route('/validate_login', methods=['POST', 'GET'])
def validate_login():
    if request.method == 'POST':
        if 'login' in request.form:
            user_name = request.form.get('username')
            password = request.form.get('password')
            db = WorkspaceData()
            data = db.get('signin', user_name)
            for s in data:
                if user_name == s['username'] and password == s['password']:
                    return redirect('/frontpage')
            return render_template('loginform.html', retry=True, errorType='login')
        elif 'signup' in request.form:
            user_name = request.form.get('username')
            password = request.form.get('password')
            email = request.form.get('email')
            db = WorkspaceData()
            db.add('signin', [(user_name, password, email)])
            return render_template('frontpage.html', retry=False, errorType='signup')


@app.route('/validate_police', methods=['POST', 'GET'])
def validate_police():
    if request.method == 'POST':
        name = request.form.get('name')
        db = WorkspaceData()
        data = db.get('companies', name)
        info_data = dict()

        for s in data:
            if name == s[0]:
                info_data['name'] = name
                info_data['info'] = s[1]
        print(info_data)
        return render_template('compsearch.html', info_data=info_data)


YOUTUBE_API_KEY = "AIzaSyDeIfyjcBEGkqy9o2Uou0dQIMIM9DLkTuM"


@app.route('/webscrap', methods=['GET', 'POST'])
def webscrap():
    search_url = 'https://www.googleapis.com/youtube/v3/search'
    video_url = 'https://www.googleapis.com/youtube/v3/videos'

    videos = []

    if request.method == 'POST':
        search_params = {
            'key': YOUTUBE_API_KEY,
            'q': request.form.get('query') + ' visual simulations',
            'part': 'snippet',
            'maxResults': 9,
            'type': 'video'
        }
        r = requests.get(search_url, params=search_params)

        results = r.json()['items']

        video_ids = []
        for result in results:
            video_ids.append(result['id']['videoId'])

        if request.form.get('submit') == 'lucky':
            return redirect(f'https://www.youtube.com/watch?v={video_ids[0]}')

        video_params = {
            'key': YOUTUBE_API_KEY,
            'id': ','.join(video_ids),
            'part': 'snippet,contentDetails',
            'maxResults': 9
        }

        r = requests.get(video_url, params=video_params)
        results = r.json()['items']
        for result in results:
            video_data = {
                'id': result['id'],
                'url': f'https://www.youtube.com/watch?v={result["id"]}',
                'thumbnail': result['snippet']['thumbnails']['high']['url'],
                'duration': int(parse_duration(result['contentDetails']['duration']).total_seconds() // 60),
                'title': result['snippet']['title'],
            }
            videos.append(video_data)
            print(video_data)

    return render_template('webscrap.html', videos=videos)


firebase = pyrebase.initialize_app(config)

db = firebase.database()


@app.route('/display', methods=['GET', 'POST'])
def display():
    if request.method == 'POST':
        if request.form['submit'] == 'add':

            name = request.form['name']
            college = request.form['college']
            mobileno = request.form['mobileno']
            address = request.form['address']
            gender = request.form['gender']
            achievements = request.form['achievements']
            state = request.form['state']
            area = request.form['area']
            email = request.form['email']
            education = request.form['education']
            print('hi')
            db.child("profiles").push(name)
            db.child("profiles").push(college)
            db.child("profiles").push(mobileno)
            db.child("profiles").push(address)
            db.child("profiles").push(gender)
            db.child("profiles").push(achievements)
            db.child("profiles").push(state)
            db.child("profiles").push(area)
            db.child("profiles").push(email)
            db.child("profiles").push(education)

            todo = db.child("profiles").get()
            to = todo.val()
            return render_template('editprofile.html', t=to.values())
        elif request.form['submit'] == 'delete':
            db.child("profiles").remove()
        return render_template('editprofile.html')
    return render_template('editprofile.html')


model = pickle.load(open('model.pkl', 'rb'))


@app.route('/percentile', methods=['POST', 'GET'])
def percentile():
    return render_template('percentile.html')


@app.route('/predict', methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    int_features = [int(x) for x in request.form.values()]
    final_features = [np.array(int_features)]
    prediction = model.predict(final_features)

    output = prediction[0]

    return render_template('percentile.html', prediction_text='percentile obtained is {}'.format(output))



@app.route('/assist', methods=['POST'])
def assist():
    text = request.get_json().get("message")
    response = finalbot(text)
    message = {"answer": response}

    if text in sent_tokens:
        sent_tokens.remove(text)

    return jsonify(message)





if __name__ == '__main__':
    app.run(debug=True)
