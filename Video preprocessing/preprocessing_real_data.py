import os
import numpy as np
from utils import extract_video_frame, img_to_video, get_video_paths, create_folder

def main():
    folder_path = "D:\\Dataset for Capstone Project\\dataset\\Celeb-DF-v2\\Celeb-real" 
    video_paths = get_video_paths(folder_path)

    save_folder = "Video preprocessing\\Processed_data\\Celeb-DF-v2\\Celeb-real"
    create_folder(save_folder)

    # Iterate each video, extract the frames which include faces 
    for video_path in video_paths:
        video_name = os.path.basename(video_path)
        video_name = save_folder + '/' + video_name
        extract_video_frame(video_path=video_path, video_name=video_name)

    '''for np_array in os.listdir(extracted_frames):
        images_array = np.load(extracted_frames + '/' + np_array)
        #frame_count = 0
        video_num = 0
        for image_array in images_array:
            face_detection(image_array, extracted_face_frames + '/' + np_array[-4], video_name=extracted_frames + '/' + (video_paths[video_num])[:-4])
            #frame_count +=1
            video_num+=1
    '''
    
    '''processed_face_video_folder = 'Video preprocessing/processed_face_videos_real'
    # Convert face frames back to video
    img_to_video(output_filename=processed_face_video_folder, fps=30, height=250, width=250, channels=3, images_folder=extracted_frames)'''

main()