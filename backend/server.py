from flask import Flask, request, render_template, jsonify
from utils import utils, registration, login
import json
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
    

@app.route("/Results", methods=["GET", "POST"])
def upload():
    if 'uploaded_file' not in request.files:
        print(request.files)
        return {'message': "No video file found"}
    video = request.files['uploaded_file']
    if video.filename == '':
        return "No selected file"
    if video and allowed_file(video.filename):
        video_path = "./static/videos/" + video.filename.split('.')[0][0:40] + ".mp4"
        audio_path = "./static/audio/" + video.filename.split('.')[0][0:40]
        video.save(video_path)
        _, audio_path = utils.extract_audio(video_path, audio_path)
        print(video_path, audio_path)
        # return render_template("frontend/src/test.js", video_name=video.filename)
        import os
        print(os.getcwd())
        print(os.listdir())
        data = "Successfuly uploaded dadada"
        return jsonify(data), 200 
    
    return {'message': "Invalid file type"}

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        print(username)
        if registration.register_user(username, password, email):
            return   # Redirect to login page after successful registration
        else:
            # Handle registration failure (e.g., user already exists)
            return render_template('register.html', error="Username already exists")


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