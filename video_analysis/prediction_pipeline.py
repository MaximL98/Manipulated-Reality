import numpy as np
from keras.models import load_model
from pathlib import Path

from video_preprocessing.utils import extract_video_frame
from video_model.feature_extractor import feature_extraction

# This main function runs the prediction pipeline, 
# given the path to where the video is save,
# the video then goes through preprocessing and feature extraction.
# Last step, loading the sequence model (MAYA) and returning the prediction
def predict(video_path):
    # Get video name using the video path
    # Example path/.../my_cool_video.mp4
    # video_name = my_cool_video
    video_name = Path(video_path).stem

    # Using the frame extraction and face detection algorithm from video_preprocessing.utils
    print(f'Starting to extract {video_name} file...')
    video_frames = extract_video_frame(video_path=video_path, video_name= "video_analysis/test_videos/" + video_name)
    # Extracting features from each frame, using pre-trained model.
    print("Extracting video features...")
    frames_features = feature_extraction(video_frames)
    # Loading already trained model (MAYA)
    print("Loading MAYA")
    maya_model = load_model("video_analysis/models/maya_model.h5")
    # Prediction on the feature extracted frames 
    prediction = maya_model.predict(frames_features)
    # The model returns the probability of the video been REAL
    # Meaning if the prediction is higher then 50% (0.5) we label as REAL else FAKE
    print("Real") if prediction > 0.5 else print("Fake")
    return prediction