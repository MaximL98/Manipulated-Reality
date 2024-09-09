import numpy as np
import keras
from keras.models import load_model


# Hyperparameters
IMG_SIZE = 224
MAX_SEQ_LENGTH = 200
NUM_FEATURES = 2048


# Function that defines the feature extractor (CNN based) model
def build_feature_extractor(fine_tuned_model):
    # Use the fine-tuned model as the base for the feature extractor
    feature_extractor = fine_tuned_model
    # Import the preprocessing function for InceptionV3
    preprocess_input = keras.applications.inception_v3.preprocess_input
    # Create an input layer for images with the specified size and channels
    inputs = keras.Input((IMG_SIZE, IMG_SIZE, 3))
    # Preprocess the input images using the InceptionV3 preprocessing function
    preprocessed = preprocess_input(inputs)
    # Extract features from the preprocessed images using the fine-tuned model
    outputs = feature_extractor(preprocessed)
    # Create a Keras Model instance with the input and output layers
    return keras.Model(inputs, outputs, name="feature_extractor")


def feature_extraction(video_frames):
    extraction_model_path = 'video_analysis/models/inceptionv3_tuned_model.keras'
    fine_tuned_model = load_model(extraction_model_path)
    if not fine_tuned_model:
        print("Error loading fine tuned model, please make sure the model in the right directory")
    feature_extractor = build_feature_extractor(fine_tuned_model)
    if not feature_extractor:
        print("Error building the feature extractor")
    # Load video frames
    video_frames = np.array(video_frames)
    frames = video_frames[None, ...] # Add batch dimension

    # Initialize an array to store extracted features
    frame_features = np.zeros(shape=(1, MAX_SEQ_LENGTH, NUM_FEATURES), dtype="float16")

    # Extract features from the frames of the current video.
    for i, batch in enumerate(frames):
        video_length = batch.shape[0]
        length = min(MAX_SEQ_LENGTH, video_length)  # Limit the number of frames to MAX_SEQ_LENGTH
        for j in range(length):
            frame_features[i, j, :] = feature_extractor.predict(batch[None, j, :])  # Extract features for each frame

    return frame_features