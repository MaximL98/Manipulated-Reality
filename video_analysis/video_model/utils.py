import random

import numpy as np
from keras import layers
import pandas as pd

from model_layers import ResidualMain, Project

# Checks if the number of feature maps in the input and the block's output differ
def add_residual_block(input, filters, kernel_size):

  out = ResidualMain(filters, 
                     kernel_size)(input)

  res = input
  # Using the Keras functional APIs, project the last dimension of the tensor to
  # match the new filter size
  if out.shape[-1] != input.shape[-1]:
    res = Project(out.shape[-1])(res)

  return layers.add([res, out])




# This function generates batches of data for training, testing and validation from a CSV file.
# Grouping multiple data samples together before feeding them into your model for training
def batch_generator(csv_file, batch_size, is_training=True):
  # Read data from csv file
  data = pd.read_csv(csv_file)
  data_list = list(zip(data['video_path'], data['label']))

  # Shuffle data for each epoch (if training)
  if is_training:
    random.shuffle(data_list)

  for i in range(0, len(data_list), batch_size):
    batch_data = data_list[i:i+batch_size]
    batch_video_paths, batch_labels = zip(*batch_data)  # Unpack into separate lists
    # Load video frames based on paths...
    batch_videos = []
    for path in batch_video_paths:
      video_frames = np.load(path)
      batch_videos.append(video_frames)
     
        
    batch_videos = np.array(batch_videos)
    print(batch_videos.shape)


    yield batch_videos, batch_labels

def load_data_from_csv(csv_path):
  data = pd.read_csv(csv_path)
  video_paths = data['video_path']
  labels = data['label']
  video_frames = []
  for path in video_paths:
    video_frame = np.load(path)
    video_frames.append(video_frame)
  return video_frames, labels


def pad_data(csv_path):
  # Read data from csv file
  data = pd.read_csv(csv_path)
  # Get only the video paths data from the csv file
  video_paths = data['video_path']
  # Set maximum video length, 225 is 15 second of video
  max_len = 225
  i = 0
  # Iterate though all video paths
  for video_path in video_paths:
    i+=1
    print(f"Starting to pad: {video_path}...")
    print(f'video number: {i} out of {len(video_paths)}')
    # Load Numpy array, which are the video frames
    video_frame = np.load(video_path)
    print(f"original shape: {video_frame.shape}")
    # Calculate by how much the video is longer or shorter then max length
    length = max_len - video_frame.shape[0]
    # If zero, save video frames as they are
    if length == 0:
      print("Video already at the desired length!")
      #np.save(video_path, video_frame)
      # Continue to next video path
      continue
    else:
      # Convert Numpy array to python list
      padding = video_frame.tolist()
      # If original video too long, remove last frames until he matches max length 
      if length < 0:
        length = abs(length)
        for i in range(length):
          padding.pop()
        np.save(video_path, padding)
        continue
      # Else, if video too short pad him with zeros (black frames)
      else:
        tmp_array = np.zeros((1, video_frame.shape[1], video_frame.shape[2], 3))
        for i in range(length):
          padding.append(tmp_array[0])
        np.save(video_path, padding)

