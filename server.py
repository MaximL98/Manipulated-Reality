from flask import Flask, request, render_template, jsonify
from backend.utils import utils, registration, login
import json
import numpy as np

import os

from video_analysis import prediction_pipeline
from AudioTraining import predictSingleAudioFile
from backend.utils.db_control import append_data, extract_user_data


ALLOWED_FILETYPES_VIDEO = ['mp4', 'avi', 'mkv', 'mov']
ALLOWED_FILETYPES_AUDIO = ['mp3', 'wav']

app = Flask(__name__, template_folder='../frontend/src/templates')

def allowed_file_video(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_FILETYPES_VIDEO

def allowed_file_audio(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_FILETYPES_AUDIO

# API Route
@app.route("/")
def App():
    return {
        render_template("App.js")
    }
   
# # Test Route 
# @app.route("/test", methods=["GET", "POST"])
# def test():
#     if 'uploaded_file' not in request.files:
#         return {'message': "No video file found"}
#     video = request.files['uploaded_file']
#     if video.filename == '':
#         print("No selected file")
#         return "No selected file"
#     if video and allowed_file(video.filename):
#         video_path = "backend/static/videos/" + video.filename.split('.')[0][0:40] + ".mp4"
#         audio_path = "backend/static/audio/" + video.filename.split('.')[0][0:40] + ".mp3"
#         video.save(video_path)
#         _, audio_path = utils.extract_audio(video_path, audio_path)
#         print("response now")
#     return jsonify(["/backend", "backend/static/sss"] ), 200 
#     return {'message': "Invalid file type"}
#     return jsonify(["/backend", "backend/static/sss"] ), 200 
    

@app.route("/Uploaded", methods=["GET", "POST"])
def upload():
    if 'uploaded_file' not in request.files:
        return {'message': "No file file found"}
    
    file = request.files['uploaded_file']

    if file.filename == '':
        return "No selected file"
    
    detection_type = request.form['detectionType']
    print(f"detection_type = {detection_type}")
    video_path = "backend/static/videos/" + file.filename.split('.')[0][0:40] + ".mp4"
    audio_path = "backend/static/audio/" + file.filename.split('.')[0][0:40] + ".mp3"

    if file:
        if detection_type == 'va':
            if allowed_file_video(file.filename):
                print("Video and audio")
                file.save(video_path)
                utils.extract_audio(video_path, audio_path)
                return jsonify([video_path, audio_path]), 200
            
        if detection_type == 'v':
            if allowed_file_video(file.filename):
                print("Video only")
                file.save(video_path)
                return jsonify([video_path, "None"]), 200
        else:
            if allowed_file_audio(file.filename):
                print("Audio only")
                file.save(audio_path)
                return jsonify(["None", audio_path]), 200
            
            elif allowed_file_video(file.filename):
                file.save(video_path)
                utils.extract_audio(video_path, audio_path)
                os.remove(video_path)
                return jsonify(["None", audio_path]), 200
            
        return {'message': "Invalid file type"}


@app.route("/Results", methods=["GET", "POST"])
def result(): 
    audio_path = request.form['audioURL']
    video_path = request.form['videoURL']
    detection_type = request.form['detectionType']
    username = request.form['username']
    print("detection type: " ,detection_type)
    print(video_path, audio_path)
    
    if video_path != "None" and audio_path != "None":
        video_result = prediction_pipeline.predict(video_path)
        audio_result = predictSingleAudioFile.predict_single_audio_file(audio_path)
        data = [video_result, audio_result]
        video_path_insert = video_path.replace('/', '.')
        append_data(username, detection_type, video_path_insert.split('.')[-2], "some path",(video_result + audio_result)/2)

    elif video_path != "None":
        video_result = prediction_pipeline.predict(video_path)
        data = [video_result]
        video_path_insert = video_path.replace('/', '.')
        append_data(username, detection_type, video_path_insert.split('.')[-2], "some path",(video_result))

    elif audio_path != "None":
        audio_result = predictSingleAudioFile.predict_single_audio_file(audio_path)
        data = [audio_result]
        audio_path_insert = audio_path.replace('/', '.')
        print(audio_path_insert)
        append_data(username, detection_type, audio_path_insert.split('.')[-2], "some path",(audio_result))

    else:
        return "Error, both of the paths are None!"
    
    # return render_template("frontend/src/test.js", video_name=video.filename)
    # video_result = prediction_pipeline.predict(video_path)
    # video_result = 0.77
    # audio_result = predictSingleAudioFile.predict_single_audio_file(audio_path)

    # data = [video_result, audio_result]
        
    # video_path_insert = video_path.replace('/', '.')
    # append_data(username, detection_type, video_path_insert.split('.')[-2], "some path",(video_result + audio_result)/2)

    if os.path.exists(audio_path):
        os.remove(audio_path)

    if os.path.exists(video_path):
        os.remove(video_path)

    return jsonify(data), 200 




@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

    if username and password and email:
        if registration.register_user(username, password, email):
            return jsonify("USER REGISTERED"), 200 # Redirect to login page after successful registration
        else:
            # Handle registration failure (e.g., user already exists)
            return jsonify("ERROR, username or email already used."), 200
    else:
        return jsonify("ERROR, please fill up all fields!"), 200


@app.route('/loginUser', methods=['GET', 'POST'])
def loginUser():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

    if username and password:
        if login.authenticate_user(username, password):
            # Redirect to protected area or home page
            return jsonify("USER FOUND"), 200
        else:
            # Handle login failure (e.g., incorrect credentials)
            return  jsonify("USER NOT FOUND"), 200
    else:
        return jsonify("ERROR, please fill up all fields!"), 200

@app.route('/user_data', methods=['GET','POST'])
def get_user_data():
    if request.method == 'POST':
        username = request.form['username']
        user_data = extract_user_data(username)
        if user_data:
            return jsonify(user_data), 200
        else:
            return jsonify("ERROR, user not found!")

if __name__ == "__main__":
    app.run(debug=True)
    