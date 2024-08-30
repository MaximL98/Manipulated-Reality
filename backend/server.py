from flask import Flask, request, render_template
from utils import utils

ALLOWED_FILETYPES = ['mp4', 'avi', 'mkv', 'mov']

app = Flask(__name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_FILETYPES

# API Route
@app.route("/")
def App():
    return {
        render_template("App.js")
    }

@app.route("/upload", methods=["POST"])
def upload():
    if 'video' not in request.files:
        print(request.files)
        return "No video file found"
    video = request.files['video']
    if video.filename == '':
        return "No selected file"
    if video and allowed_file(video.filename):
        video_path = "./static/videos/" + video.filename.split('.')[0] + ".mp4"
        audio_path = "./static/audio/" + video.filename.split('.')[0]
        video.save(video_path)
        video_path, audio_path = utils.extract_audio(video_path, audio_path)
        print(video_path, audio_path)
        # return render_template("frontend/src/test.js", video_name=video.filename)
        return "Uploaded succesfuly"
    return "Invalid file type"
    
if __name__ == "__main__":
    app.run(debug=True)