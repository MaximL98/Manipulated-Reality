import cv2
import os
import numpy as np
import face_recognition
from PIL import Image


def extract_video_frame(video_path, video_name):
    print(video_name + "_frames.npy")
    if os.path.exists(video_name + "_frames.npy"):
        print(f"Numpy array for this file {video_name} already exists!")
        return

    # Create a VideoCapture object to read the video
    cap = cv2.VideoCapture(video_path)
    # Check if the video was opened successfully
    if not cap.isOpened():
        print("Error opening video!")
        return None

    # Get video properties
    '''width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Create an empty NumPy array to store the frames
    frames = np.empty((int(cap.get(cv2.CAP_PROP_FRAME_COUNT)), height, width, 3), dtype=np.uint8)
    '''
    # Get video properties
    width = 150
    height = 150

    # Create an empty NumPy array to store the frames
    frames = np.empty((int(cap.get(cv2.CAP_PROP_FRAME_COUNT)), height, width, 3), dtype=np.uint8)

    # Process each frame of the video
    frame_count = 0
    print(f'Starting to extract {video_name} file...')
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        
        # Check if the frame was read correctly
        if not ret:
            print("No more frames to capture!")
            break
        
        # Convert frame to RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        face_frame = face_detection(frame, width, height)

        if face_frame.size != 0:
            #Add the frame to the NumPy array
            frames[frame_count] = face_frame
            frame_count += 1

            
    # Release the capture and close all windows
    cap.release()

    if video_name:
        print(f"Saving video frame as numpy array as {video_name}_frames.npy")
        np.save(f"{video_name}_frames.npy", frames)

    #return frames



def face_detection(image_array, width, height):
    face_locations = face_recognition.face_locations(image_array)
    empty_array = np.array([])
    if face_locations:
        top, right, bottom, left = face_locations[0]

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



def get_video_paths(folder_path):
  """
  This function retrieves the full paths of all video files within a directory.

  Args:
      folder_path (str): The path to the directory containing the videos.

  Returns:
      list: A list of strings representing the full paths of all video files.
  """

  video_paths = []
  for root, _, files in os.walk(folder_path):
    for file in files:
      if os.path.splitext(file)[1].lower() in ('.mp4', '.avi', '.mov', '.wmv'):  # Common video extensions
        video_path = os.path.join(root, file)
        video_paths.append(video_path)
  return video_paths


def create_folder(folder_path):
    try:
        os.makedirs(folder_path, exist_ok=True)
        print("Folder created successfully!")
    except OSError as error:
        print(f"Error creating folder: {error}")




def img_to_video(output_filename, fps, height, width, channels, images_folder):
    # Set the fourcc code for video format (e.g., MP4)
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")


    # Get the dimensions of the first image (assuming all images have same size)
    '''image_path = "image1.jpg"  # Replace with path to your first image
    image = cv2.imread(image_path)
    height, width, channels = image.shape'''

    video = cv2.VideoWriter(output_filename, fourcc, fps, (width, height))

    for filename in os.listdir(images_folder):
        if filename.endswith(".jpg"):  # Check image extensions
            image_path = os.path.join(images_folder, filename)
            image = cv2.imread(image_path)

            # Resize image to target resolution
            resized_image = cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)

            video.write(resized_image)

    video.release()
    print("Video created successfully!")


