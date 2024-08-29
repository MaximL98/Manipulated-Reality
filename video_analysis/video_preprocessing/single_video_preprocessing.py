import cv2
import numpy as np
import face_recognition

import os

# Function to extract video frames, later face frames and save them as npy files.
def extract_video_frame(video_path, video_name):
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
    error_detect = 0
    # Process each frame of the video
    try:
        while True:
            # Capture frame-by-frame
            ret, frame = cap.read()
            # Target time interval between frames in milliseconds
            target_fps = 15
            
            # # In some of the videos in the real dataset are originally slowed down by x2
            # # To deal with that, x2 fps will be taken
            # if '#' in video_name:
            #     target_fps = 30

            subsample_rate = int(1000 / target_fps)  # Convert FPS to milliseconds
            # Move to the next frame based on the subsample rate
            cap.set(cv2.CAP_PROP_POS_MSEC, (cap.get(cv2.CAP_PROP_POS_MSEC) + subsample_rate))
            # Check if the frame was read correctly
            if not ret:
                print("No more frames to capture!")
                break

            # Convert frame to RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Apply face detection algorithm on the frame
            face_frame = face_detection(frame, width, height)
            print(f"Frame {len(frames) + 1} / 200")

            # If no face detected
            if face_frame.size == 0:
                error_detect += 1
                # If more then 100 frames in row did not include face
                # The video will be label invalid
                if error_detect > 100:
                    raise Exception("Sorry, bad video input. No faces detected!")

            if face_frame.size != 0:
                frames.append(face_frame)

            # Maximum seq length
            if len(frames) == 200:
                break

    finally:
        # Release the capture and close all windows
        cap.release()

    # Return the processed frames as npy array
    if video_name:
        return frames


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
