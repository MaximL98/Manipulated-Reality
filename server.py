from flask import Flask, request, render_template, jsonify
from backend.utils import utils

import os

from video_analysis import prediction_pipeline
from AudioTraining import predictSingleAudioFile
from backend.utils.db_control import append_data, extract_user_data, register_user, authenticate_user


ALLOWED_FILETYPES_VIDEO = ['mp4', 'avi', 'mkv', 'mov']
ALLOWED_FILETYPES_AUDIO = ['mp3', 'wav']

app = Flask(__name__, template_folder='../frontend/src/templates')
# Function that checks if the file type is an video format
def allowed_file_video(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_FILETYPES_VIDEO
# Function that checks if the file type is an audio format
def allowed_file_audio(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_FILETYPES_AUDIO

# API Route
@app.route("/")
def App():
    return {
        render_template("App.js")
    }
   
# Function that handles upload page
@app.route("/Uploaded", methods=["GET", "POST"])
def upload():
    # Check if file was uploaded successfully 
    if 'uploaded_file' not in request.files:
        return {'message': "No file file found"}
    try:
        file = request.files['uploaded_file']

        if file.filename == '':
            return "No selected file"
        # Get user selected detection type from the frontend
        detection_type = request.form['detectionType']
        print(f"detection_type = {detection_type}")
        # Set video and audio paths
        video_path = "backend/static/videos/" + file.filename.split('.')[0][0:40] + ".mp4"
        audio_path = "backend/static/audio/" + file.filename.split('.')[0][0:40] + ".mp3"
    except:
        return {'message': "File not found or corrupted!"}
    # If file not corrupted
    if file:
        # Check if selected detection type is video & audio
        if detection_type == 'va':
            if allowed_file_video(file.filename):
                print("Video and audio")
                # Save the video locally
                file.save(video_path)
                # Extract audio from the video
                paths = utils.extract_audio(video_path, audio_path)
                # Check if the video had audio in it
                if not paths:
                    return jsonify([video_path]), 200
                return jsonify([video_path, audio_path]), 200
        # Check if detection type is video only
        if detection_type == 'v':
            if allowed_file_video(file.filename):
                print("Video only")
                file.save(video_path)
                return jsonify([video_path]), 200
        # Check if detection type is audio only
        else:
            # Check if file format is audio
            if allowed_file_audio(file.filename):
                print("Audio only")
                file.save(audio_path)
                return jsonify([audio_path]), 200
            # Check if file format is video
            elif allowed_file_video(file.filename):
                file.save(video_path)
                # Extract audio from the video
                paths = utils.extract_audio(video_path, audio_path)
                # Delete the video
                os.remove(video_path)
                if not paths:
                    return jsonify(), 200
                return jsonify([audio_path]), 200
            
        return {'message': "Invalid file type"}
    return {'message': "File not found!"}

# Function that handles the result page
@app.route("/Results", methods=["GET", "POST"])
def result(): 
    # Get video and audio paths, detection type and username from the frontend
    audio_path = request.form['audioURL']
    video_path = request.form['videoURL']
    detection_type = request.form['detectionType']
    username = request.form['username']
    print("detection type: " ,detection_type)
    print(video_path, audio_path)
    # If there is both video and audio paths then run detection both on video and audio models
    if video_path != "undefined" and audio_path != "undefined":
        video_result = prediction_pipeline.predict(video_path)
        audio_result = predictSingleAudioFile.predict_single_audio_file(audio_path)
        data = [video_result, audio_result]
        video_path_insert = video_path.replace('/', '.')
        # Save results into the database
        append_data(username, "Video & Audio", video_path_insert.split('.')[-2], "some path",(video_result + audio_result)/2)
    # If only video path, run detection only on the video model
    elif video_path != "undefined":
        video_result = prediction_pipeline.predict(video_path)
        data = [video_result]
        video_path_insert = video_path.replace('/', '.')
        # Save results into the database
        append_data(username, "Video", video_path_insert.split('.')[-2], "some path",(video_result))
    # if only audio path, run detection only on the audio model
    elif audio_path != "undefined":
        print(f"audio_path={audio_path}")
        audio_result = predictSingleAudioFile.predict_single_audio_file(audio_path)
        data = [audio_result]
        audio_path_insert = audio_path.replace('/', '.')
        print(audio_path_insert)
        # Save results into the database
        append_data(username, "Audio", audio_path_insert.split('.')[-2], "some path",(audio_result))
    # If no path found return error
    else:
        print("Error, both of the paths are None!")
        return "Error, both of the paths are None!"
    # Remove audio and video files that were saved locally if there is
    if os.path.exists(audio_path):
        os.remove(audio_path)

    if os.path.exists(video_path):
        os.remove(video_path)

    return jsonify(data), 200 

# Function that handles registration page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get username, password and email from the frontend
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
    # Check if user input all the needed fields 
    if username and password and email:
        # If registration was successful 
        if register_user(username, password, email):
            return jsonify("USER REGISTERED"), 200 # Redirect to login page after successful registration
        else:
            # Handle registration failure (e.g., user already exists)
            return jsonify("ERROR, username or email already used."), 200
    else:
        return jsonify("ERROR, please fill up all fields!"), 200

# Function that handles login page
@app.route('/loginUser', methods=['GET', 'POST'])
def loginUser():
    if request.method == 'POST':
        # Get username and password from the frontend
        username = request.form['username']
        password = request.form['password']
    # Check if user input all the needed fields
    if username and password:
        # Authenticate the username and the password that he exists in the database
        if authenticate_user(username, password):
            # Redirect to protected area or home page
            return jsonify("USER FOUND"), 200
        else:
            # Handle login failure (e.g., incorrect credentials)
            return  jsonify("USER NOT FOUND"), 200
    else:
        return jsonify("ERROR, please fill up all fields!"), 200

# Function that handles extraction of user data for the profile page
@app.route('/user_data', methods=['GET','POST'])
def get_user_data():
    if request.method == 'POST':
        # Get username from the frontend
        username = request.form['username']
        # Extract user data from the database, based on his username
        user_data = extract_user_data(username)
        if user_data:
            return jsonify(user_data), 200
        else:
            return jsonify("ERROR, user not found!")

if __name__ == "__main__":
    app.run(debug=True)
    