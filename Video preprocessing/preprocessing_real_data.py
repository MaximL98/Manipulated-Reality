import os
import numpy as np
from utils import extract_video_frame, img_to_video, face_detection

def main():
    # Path to real videos
    real_data_folder = 'Video preprocessing/real_videos'

    # List to hold all video paths
    video_paths = []
    frames_array = []
    # Iterate every video file and save its path

    # Variables needed for extracting frames from video
    extracted_frames = 'Video preprocessing/extracted_frames_real'
    extracted_face_frames = 'Video preprocessing/extracted_face_frames_real'

    # Iterate each video, extract the frames which include faces 
    '''for video_path in os.listdir(real_data_folder):
        extract_video_frame(video_path=real_data_folder + '/' + video_path, video_name=extracted_frames + '/' + video_path[:-4])
    '''
    for np_array in os.listdir(extracted_frames):
        images_array = np.load(extracted_frames + '/' + np_array)
        frame_count = 0
        for image_array in images_array:
            face_detection(image_array, extracted_face_frames + '/' + np_array[-4], frame_count)
            frame_count +=1
    
    '''processed_face_video_folder = 'Video preprocessing/processed_face_videos_real'
    # Convert face frames back to video
    img_to_video(output_filename=processed_face_video_folder, fps=30, height=250, width=250, channels=3, images_folder=extracted_frames)'''


main()