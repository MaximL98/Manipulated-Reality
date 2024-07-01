from pathlib import Path

from utils import extract_video_frame, get_video_paths, create_folder
from data import folder_path_to_datasets, paths_to_folders_after_processing

# Main function
def main():
    # List of paths to the dataset
    folder_paths = [folder_path_to_datasets['celeb_DF_real'], 
                    folder_path_to_datasets['celeb_DF_fake']]
    # List of paths to folders into which after processing the npy files will be saved
    save_folders = [paths_to_folders_after_processing ['celeb_DF_real'],
                    paths_to_folders_after_processing['celeb_DF_fake']]
    # For loop, process both real and fake data
    for index in range(len(folder_paths)):
        # Path to folder which contains data
        folder_path = folder_paths[index]
        # Path to folder in which processed data will be saved
        save_folder = save_folders[index]
        # List of available types in which the data was split
        types = ["train", "test", "val"]
        for type in types:
            # Get paths of all videos
            video_paths = get_video_paths(folder_path + '/' + type)
            # If such folder does not exist, create it
            tmp_save_folder = save_folder  + '/' + type
            create_folder(tmp_save_folder)
            # Initialize index to follow how many videos finished processing
            i = 0
            # Get total number of files in a folder
            num_files = len(video_paths)
            # For smaller model process only 10-20% of the data, for full model 100%
            num_to_process = int(num_files*0.1)
            # Iterate each video, extract the frames which include faces
            for video_path in video_paths:
                if i == num_to_process:
                    print(f"Reached set limit of {num_to_process} out of {num_files}")
                    break;
                print(f"Video {i + 1}/{num_files}")
                # Get video name
                video_name = Path(video_path).stem
                video_name = tmp_save_folder + '/' + video_name
                # Preprocess the video
                extract_video_frame(video_path=video_path, video_name=video_name)
                i+=1

main()