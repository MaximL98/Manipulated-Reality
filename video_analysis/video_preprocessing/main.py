# Import time to calculate how long normalization step takes
import time

from pathlib import Path

from utils import label_data, normalize_frames, create_normalization_folders
from data import processed_data_folder_paths

# Main function to split and normalize the data
def main():
    # Path to fake and real data, after frame extraction and face recognition
    fake_video_folder_train = processed_data_folder_paths['fake_video_folder_train']
    fake_video_folder_test = processed_data_folder_paths['fake_video_folder_test']
    fake_video_folder_val = processed_data_folder_paths['fake_video_folder_val']

    real_video_folder_train = processed_data_folder_paths['real_video_folder_train']
    real_video_folder_test = processed_data_folder_paths['real_video_folder_test']
    real_video_folder_val = processed_data_folder_paths['real_video_folder_val']
    # Label the data
    train_df, test_df, val_df = label_data(real_train_folder=real_video_folder_train, real_test_folder=real_video_folder_test, real_val_folder=real_video_folder_val, 
              fake_train_folder=fake_video_folder_train, fake_test_folder=fake_video_folder_test, fake_val_folder=fake_video_folder_val)

    # Create normalization folders, to which the data will be saved
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
            #print("--- %s seconds ---" % (time.time() - start_time))
            

if __name__ == '__main__':
    main()






