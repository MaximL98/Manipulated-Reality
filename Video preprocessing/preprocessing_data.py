from pathlib import Path
from utils import extract_video_frame, get_video_paths, create_folder
from data import folder_path_to_datasets

# Main function
def main():
    # List of paths to the dataset
    folder_paths = [folder_path_to_datasets['celeb_DF_real'], 
                    folder_path_to_datasets['celeb_DF_fake']]
    # List of paths to folders into which after processing the npy files will be saved
    save_folders = ["Video preprocessing/Processed_data_real/Celeb-DF-v2/Celeb-real"
                   ,"Video preprocessing/Processed_data_fake/Celeb-DF-v2/Celeb-synthesis"]
    # For loop, process both real and fake data
    for index in range(len(folder_paths)):
        # Path to folder which contains data
        folder_path = folder_paths[index]
        # Path to folder in which processed data will be saved
        save_folder = save_folders[index]
        # List of availble types in which the data was split
        types = ["train", "test", "val"]
        for type in types:
            # Get paths of all videos
            video_paths = get_video_paths(folder_path + '/' + type)
            # If such folder does not exist, create it
            save_folder = save_folder  + '/' + type
            create_folder(save_folder)
            # Initialize index to follow how many videos finished processing
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