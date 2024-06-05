import cv2
import os
import numpy as np
import face_recognition


def extract_video_frame(video_path, video_name):
    # Create a VideoCapture object to read the video
    cap = cv2.VideoCapture(video_path)
    # Check if the video was opened successfully
    if not cap.isOpened():
        print("Error opening video!")
        return None

    # Get video properties
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

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

        '''# Save the frame as an image (optional)
        frame_name = f'{video_name}_{frame_count:05d}.jpg'
        cv2.imwrite(frame_name, frame)'''

        # Display the frame for debugging (optional)
        # cv2.imshow('Frame', frame)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break

        #Add the frame to the NumPy array
        frames[frame_count] = frame

        frame_count += 1

    # Release the capture and close all windows
    cap.release()
    # cv2.destroyAllWindows()  # If you used cv2.imshow()
    if video_name:
        print(f"Saving video frame as numpy array as {video_name}_frames.npy")
        np.save(f"{video_name}_frames.npy", frames)

    #return frames



def face_detection(image_array):
    import face_recognition
from PIL import Image  # Import for PIL image creation

def face_detection(image_array, save_path, frame_count):
    # Detect faces in the image
    face_locations = face_recognition.face_locations(image_array)

    if face_locations:  # Check if any faces were detected
        # Extract the first face location (assuming single face detection)
        top, right, bottom, left = face_locations[0]

        try:
            # Extract the face image from the original array
            face_image = image_array[top:bottom, left:right]

            # Create a PIL image from the extracted face array
            pil_image = Image.fromarray(face_image)

            # Save the extracted face image
            pil_image.save(f"{save_path}_{frame_count:05d}.jpg")

            return True  # Indicate successful face detection and saving

        except IndexError:  # Handle potential index errors (e.g., out-of-bounds)
            print("Error: Could not extract face due to invalid bounding box coordinates.")
            return False  # Indicate failure

    else:
        print("No faces detected in the image.")
        return False  # Indicate no faces found






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


