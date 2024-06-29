import cv2
import os
import numpy as np
import face_recognition
import pandas as pd
import torchvision.transforms as transforms

from sklearn.model_selection import train_test_split
# Imports paths from data file
from data import paths_to_folders_after_normalization, paths_to_csv


# Function to extract video frames, later face frames and save them as npy files.
def extract_video_frame(video_path, video_name):
    # Check if file was all ready processed
    if os.path.exists(video_name + "_processed.npy"):
        print(f"Numpy array for this file {video_name} already exists!")
        return

    # Create a VideoCapture object to read the video
    cap = cv2.VideoCapture(video_path)
    # Check if the video was opened successfully
    if not cap.isOpened():
        print("Error opening video!")
        return None

    # Video properties
    width = 224
    height = 224

    # Empty array to store the frames
    frames = []

    print(f'Starting to extract {video_name} file...')
    # Process each frame of the video
    try:
        while True:
            # Capture frame-by-frame
            ret, frame = cap.read()
            # Target time interval between frames in milliseconds
            target_fps = 15
            subsample_rate = int(1000 / target_fps)  # Convert FPS to milliseconds
            # Move to the next frame based on the subsample rate
            cap.set(cv2.CAP_PROP_POS_MSEC, (cap.get(cv2.CAP_PROP_POS_MSEC) + subsample_rate))
            # Check if the frame was read correctly
            if not ret:
                print("No more frames to capture!")
                break
            
            # Convert frame to RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            face_frame = face_detection(frame, width, height)

            if face_frame.size != 0:
                frames.append(face_frame)
            
            # Can later set higher number of frames
            '''if len(frames) == 400:
                break'''

    finally:   
        # Release the capture and close all windows
        cap.release()

    # Save the processed frames as npy array
    if video_name:
        print(f"Saving video frame as numpy array as {video_name}_processed.npy")
        np.save(f"{video_name}_processed.npy", frames)


# Function that implement face recognition in a frame
def face_detection(image_array, width, height):
    # Locate faces in the frame
    face_locations = face_recognition.face_locations(image_array)
    # Empty numpy array to return in case of not faces were detected
    empty_array = np.array([])
    # Check if face was detected in the frame
    if face_locations:
        top, right, bottom, left = face_locations[0]
        # Save the face frame and resize it
        try:
            face_frame = image_array[top:bottom, left:right]
            resized_face_frame = cv2.resize(face_frame, (width, height), interpolation=cv2.INTER_AREA)
            return resized_face_frame

        except IndexError:
            print("Error: Could not extract face due to invalid bounding box coordinates.")
            return empty_array  # Indicate failure

    else:
        print("No faces detected in the image.")
        return empty_array  # Indicate no faces found


# Function that returns array of strings representing the full paths of all video files
def get_video_paths(folder_path):
  video_paths = []
  # Look into all files inside the path and return all the paths of video files
  for root, _, files in os.walk(folder_path):
    for file in files:
      if os.path.splitext(file)[1].lower() in ('.mp4', '.avi', '.mov', '.wmv', '.npy'):  # Common video extensions and npy
        video_path = os.path.join(root, file)
        video_paths.append(video_path)
  return video_paths

#!!!# The following two split functions purpose is automation of files handling only #!!!#
# Function that automates splitting data into train, test, val folders
def split_data(folder_path, train_ratio=0.6, test_ratio=0.2, val_ratio=0.2):
    # Check if the ratio covers all videos
    if train_ratio + val_ratio + test_ratio != 1:
        raise ValueError("Sum of ratios must equal 1.")

    files = os.listdir(folder_path)

    train_size = int(len(files) * train_ratio)
    val_size = int(len(files) * val_ratio)

    train_data = files[:train_size]
    val_data = files[train_size:train_size + val_size]
    test_data = files[train_size + val_size:]

    # Create subdirectories for each set
    os.makedirs(os.path.join(folder_path, "train"), exist_ok=True)
    os.makedirs(os.path.join(folder_path, "val"), exist_ok=True)
    os.makedirs(os.path.join(folder_path, "test"), exist_ok=True)

    # Move files to respective subdirectories
    for filename in train_data:
        os.rename(os.path.join(folder_path, filename), os.path.join(folder_path, "train", filename))

    for filename in val_data:
        os.rename(os.path.join(folder_path, filename), os.path.join(folder_path, "val", filename))

    for filename in test_data:
        os.rename(os.path.join(folder_path, filename), os.path.join(folder_path, "test", filename))

    print("Data split completed!")


# Function to move files from one folder to another
def split_data_v2(splitted_folder_path, to_split_folder_path, type):
    files = os.listdir(splitted_folder_path)
    
    # Create subdirectories for each set
    os.makedirs(os.path.join(to_split_folder_path, type), exist_ok=True)

    # Process data from other_data_dir
    
    for filename in os.listdir(to_split_folder_path):
        for f in files:
            if (filename[:4] == f[:4]):
                print(f"filename = {filename}")
                print(f"f = {f}")
                # Move files with matching prefix to train directory
                os.rename(os.path.join(to_split_folder_path, filename), os.path.join(to_split_folder_path, type, filename))
                break


# Function to create folder
def create_folder(folder_path):
    try:
        os.makedirs(folder_path, exist_ok=True)
        print("Folder created successfully!")
    except OSError as error:
        print(f"Error creating folder: {error}")


# Function to split the dataset into train, test and, validation
def split_train_test_data(real_video_folder, fake_video_folder, test_size=0.2, val_size=0.2):
    # Lists to store file paths and labels
    real_video_paths = get_video_paths(real_video_folder)
    fake_video_paths = get_video_paths(fake_video_folder)

    # Define labels for real and fake videos (modify if needed)
    real_labels = [1 for _ in real_video_paths]  # Label real videos as 1
    fake_labels = [0 for _ in fake_video_paths]  # Label fake videos as 0

    # Combine paths and labels into lists of tuples
    all_data = list(zip(real_video_paths + fake_video_paths, real_labels + fake_labels))
    # Combine test and validation set sizes
    total_split_size = test_size + val_size
    # Split data into training and testing sets using sklearn
    train_data, test_val_data  = train_test_split(all_data, test_size=total_split_size, random_state=42)
    val_data, test_data = train_test_split(test_val_data, test_size=test_size / total_split_size, random_state=42)
    
    # Separate features (paths) and labels (targets) in both sets
    train_features, train_targets = zip(*train_data)
    test_features, test_targets = zip(*test_data)
    val_features, val_targets = zip(*val_data)

    # Create DataFrames
    train_df = pd.DataFrame({"video_path": train_features, "label": train_targets})
    test_df = pd.DataFrame({"video_path": test_features, "label": test_targets})
    val_df = pd.DataFrame({"video_path": val_features, "label": val_targets})

    print("Train data shape:", train_df.shape)
    print("Test data shape:", test_df.shape)
    print("Validation data shape:", val_df.shape)
    return train_df, test_df, val_df


# Function to label data, after it was splitted
# If data splitting was made not using "split_train_test_data" then this function is needed to label data
def label_data(real_train_folder, real_test_folder, real_val_folder, 
              fake_train_folder, fake_test_folder, fake_val_folder):
    
    # Lists to store file paths and labels
    real_train_paths = get_video_paths(real_train_folder)
    real_test_paths = get_video_paths(real_test_folder)
    real_val_paths = get_video_paths(real_val_folder)

    fake_train_paths = get_video_paths(fake_train_folder)
    fake_test_paths = get_video_paths(fake_test_folder)
    fake_val_paths = get_video_paths(fake_val_folder)

    # Assign labels (1 for real, 0 for fake)
    real_label = 1
    fake_label = 0

    # Create DataFrames for real videos
    train_df_real = pd.DataFrame({"video_path": real_train_paths, "label": [real_label] * len(real_train_paths)})
    test_df_real = pd.DataFrame({"video_path": real_test_paths, "label": [real_label] * len(real_test_paths)})
    val_df_real = pd.DataFrame({"video_path": real_val_paths, "label": [real_label] * len(real_val_paths)})

    # Create DataFrames for fake videos
    train_df_fake = pd.DataFrame({"video_path": fake_train_paths, "label": [fake_label] * len(fake_train_paths)})
    test_df_fake = pd.DataFrame({"video_path": fake_test_paths, "label": [fake_label] * len(fake_test_paths)})
    val_df_fake = pd.DataFrame({"video_path": fake_val_paths, "label": [fake_label] * len(fake_val_paths)})

    # Combine real and fake DataFrames for each split
    train_df = pd.concat([train_df_real, train_df_fake], ignore_index=True)
    test_df = pd.concat([test_df_real, test_df_fake], ignore_index=True)
    val_df = pd.concat([val_df_real, val_df_fake], ignore_index=True)

    # Check if DataFrames were converted to csv already, comment does lines if want to update csv's
    if os.path.exists(paths_to_csv['train_df']) and os.path.exists(paths_to_csv['test_df']) and paths_to_csv['val_df']:
        print("DataFrames already converted to csv's files...")
        # Return DataFrames of train, test and valuation
        return train_df, test_df, val_df
    
    # Save DataFrame as csv file
    train_df.to_csv(paths_to_csv['train_df'], sep=',', index=False, encoding='utf-8')
    test_df.to_csv(paths_to_csv['test_df'], sep=',', index=False, encoding='utf-8')
    val_df.to_csv(paths_to_csv['val_df'], sep=',', index=False, encoding='utf-8')

    # Return DataFrames of train, test and valuation
    return train_df, test_df, val_df


# Function to normalize frames
def normalize_frames(video_path, video_name):
    # Check if file was all ready processed
    if os.path.exists(video_name + '.npy'):
        #print(f"This file ({video_name}) already normalized!")
        return
    # Load frames from video path
    frames = np.load(video_path)
    # Custom transform function
    transform = transforms.Compose([
        transforms.ToTensor()])
   
    # Initialize array to save normalized frames
    frames_normalized = []
    # Iterate each frame, perform normalization based on given mean & std values
    for frame in frames:
        # Transform the frame
        frame_transform = transform(frame)
        # Calculate mean and std
        mean, std = frame_transform.mean([1,2]), frame_transform.std([1,2])
        # Define custom transform, to calculate mean & std
        transform_norm = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize(mean, std)])
        # Get normalized frame
        frame_normalized = transform_norm(frame)
        # Convert normalized frame back to NumPy array
        frame_normalized = np.array(frame_normalized)
        # Transpose from shape of (3,,) to shape of (,,3)
        frame_normalized = frame_normalized.transpose(1, 2, 0)
        # Append normalized frame into array
        frames_normalized.append(frame_normalized)
    # Save normalized frames as npy array
    np.save(f"{video_name}.npy", frames_normalized)


# Function that creates folders into which data will be saved after normalization
# And returns their paths
def create_normalization_folders():
    # Folder paths that will be created
    train_folder = paths_to_folders_after_normalization['train_folder']
    test_folder = paths_to_folders_after_normalization['test_folder']
    val_folder = paths_to_folders_after_normalization['val_folder']

    if os.path.exists(train_folder) and os.path.exists(test_folder) and os.path.exists(val_folder):
        print("Normalization folders already exists!")
        return train_folder, test_folder, val_folder

    # Create folder to save into the normalized data
    create_folder(train_folder)
    create_folder(test_folder)
    create_folder(val_folder)
    # Return paths
    return train_folder, test_folder, val_folder
