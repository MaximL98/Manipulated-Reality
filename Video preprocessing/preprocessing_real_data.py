from pathlib import Path
from utils import extract_video_frame, get_video_paths, create_folder
from data import folder_path_to_datasets

# Main function
def main():
    # Path to folder which contains data
    folder_path = folder_path_to_datasets['celeb_DF_real']

    # Path to folder in which processed data will be saved
    save_folder = "Video preprocessing/Processed_data_real/Celeb-DF-v2/Celeb-real"
   
    types = ["train", "test", "val"]
    for type in types:
        # Get paths of all videos
        video_paths = get_video_paths(folder_path + '/' + type)
        # If such folder does not exist, create it
        save_folder = save_folder  + '/' + type
        create_folder(save_folder)

        i = 1
        # Iterate each video, extract the frames which include faces 
        for video_path in video_paths:
            print(f"Video {i}/{len(video_paths)}")
            # Get video name
            video_name = Path(video_path).stem
            video_name = save_folder + '/' + video_name
            # Preprocesse the video
            extract_video_frame(video_path=video_path, video_name=video_name)
            i+=1

main()