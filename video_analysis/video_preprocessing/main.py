# Import time to calculate how long normalization step takes
import time

from pathlib import Path

from utils import label_data, normalize_frames, create_normalization_folders, get_video_paths, create_folder
from data import processed_data_folder_paths, paths_to_folders_after_processing, paths_to_folders_after_normalization

# Main function to split and normalize the data
def main():
    folder_paths = [paths_to_folders_after_processing ['celeb_DF_real'],
                    paths_to_folders_after_processing['celeb_DF_fake']]
    
    save_folders = [paths_to_folders_after_normalization['celeb_DF_real'],
                    paths_to_folders_after_normalization['celeb_DF_fake']]
    
    # For-loop to normalize train, test and, validation datasets
    for index in range(len(folder_paths)):
        folder_path = folder_paths[index]
        save_folder = save_folders[index]
        types = ["train", "test", "val"]
        for type in types:
            i=0
            video_paths = get_video_paths(folder_path + '/' + type)
            tmp_save_folder = save_folder + '/' + type
            create_folder(tmp_save_folder)
            for video_path in video_paths:
                print(f"Video {i+1}/{len(video_paths)}")
                video_name = Path(video_path).stem
                video_name = tmp_save_folder + '/' + video_name
                # Use normalize frames function that normalizes frames and saves in the destination folder
                normalize_frames(video_path=video_path, video_name=video_name)
                i+=1

    # Path to fake and real data, after frame extraction, face recognition and normalization
    fake_video_folder_train = processed_data_folder_paths['fake_video_folder_train']
    fake_video_folder_test = processed_data_folder_paths['fake_video_folder_test']
    fake_video_folder_val = processed_data_folder_paths['fake_video_folder_val']

    real_video_folder_train = processed_data_folder_paths['real_video_folder_train']
    real_video_folder_test = processed_data_folder_paths['real_video_folder_test']
    real_video_folder_val = processed_data_folder_paths['real_video_folder_val']
    # Label the data
    label_data(real_train_folder=real_video_folder_train, real_test_folder=real_video_folder_test, real_val_folder=real_video_folder_val, 
              fake_train_folder=fake_video_folder_train, fake_test_folder=fake_video_folder_test, fake_val_folder=fake_video_folder_val)

    '''# Create normalization folders, to which the data will be saved
    train_folder, test_folder, val_folder = create_normalization_folders()
    # All DataFrames and folders
    dfs = [train_df, test_df, val_df]
    folders = [train_folder, test_folder, val_folder]
    # Loop through each DataFrame and save to a specific folder
    for index in range(3):
        # For-loop to normalize train, test and, validation datasets
        for video_path in dfs[index]['video_path']:
            #start_time = time.time()
            #print(f"Starting to normalize {video_path} ...")
            # Get video name
            video_name = Path(video_path).stem
            video_name = folders[index] + '/' + video_name
            # Use normalize frames function that normalizes frames and saves in the destination folder
            normalize_frames(video_path, video_name)
            #print("--- %s seconds ---" % (time.time() - start_time))'''

    
            

if __name__ == '__main__':
    main()






