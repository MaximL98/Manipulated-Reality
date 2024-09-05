from flask import Flask, request, render_template, jsonify
from backend.utils import utils, registration, login
import json
import numpy as np

import os

from video_analysis import prediction_pipeline
from AudioTraining import predictSingleAudioFile
from backend.utils.db_control import append_data

ALLOWED_FILETYPES = ['mp4', 'avi', 'mkv', 'mov']

app = Flask(__name__, template_folder='../frontend/src/templates')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_FILETYPES

# API Route
@app.route("/")
def App():
    return {
        render_template("App.js")
    }
   
# Test Route 
@app.route("/test", methods=["GET", "POST"])
def test():
    return jsonify("Server responded with message: " + request.form['text_file'] + " "+ request.form['text_file']), 200 
    

@app.route("/Uploaded", methods=["GET", "POST"])
def upload():
    print("here")
    if 'uploaded_file' not in request.files:
        print(request.files)
        return {'message': "No video file found"}
    video = request.files['uploaded_file']
    if video.filename == '':
        return "No selected file"
    if video and allowed_file(video.filename):
        video_path = "backend/static/videos/" + video.filename.split('.')[0][0:40] + ".mp4"
        audio_path = "backend/static/audio/" + video.filename.split('.')[0][0:40] + ".mp3"
        video.save(video_path)
        _, audio_path = utils.extract_audio(video_path, audio_path)
        
        return jsonify([video_path, audio_path]), 200
    return {'message': "Invalid file type"}


@app.route("/Results", methods=["GET", "POST"])
def result(): 
    if request.form['count'] == 1:
        return jsonify("Already done"), 200
    audio_path = request.form['audioURL']
    video_path = request.form['videoURL']
    #detection_type = request.form['detection_type']
    print(video_path, audio_path)
    # return render_template("frontend/src/test.js", video_name=video.filename)
    # video_result = prediction_pipeline.predict(video_path)
    video_result = 0.77
    audio_result = predictSingleAudioFile.predict_single_audio_file(audio_path)

    data = [video_result, audio_result]
    
    USERNAME = 'c1'
    DETECTION_TYPE = 'V&A'

    video_path_insert = video_path.replace('/', '.')
    append_data(USERNAME, DETECTION_TYPE, video_path_insert.split('.')[-2], (video_result + audio_result)/2)

    if os.path.exists(audio_path) and os.path.exists(video_path):
        os.remove(audio_path)
        os.remove(video_path)
    else:
        print("One of the files does not exists.") 

    return jsonify(data), 200 




@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        if registration.register_user(username, password, email):
            return "USER REGISTERED" # Redirect to login page after successful registration
        else:
            # Handle registration failure (e.g., user already exists)
            return "ERROR, username or email already used."


@app.route('/loginUser', methods=['GET', 'POST'])
def loginUser():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']


        if login.authenticate_user(username, password):
            # Redirect to protected area or home page
            return "USER FOUND"
        else:
            # Handle login failure (e.g., incorrect credentials)
            return "USER NOT FOUND"

   
if __name__ == "__main__":
    app.run(debug=True)