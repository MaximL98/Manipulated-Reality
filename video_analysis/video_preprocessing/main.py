import numpy as np
from pathlib import Path

from utils import label_data, normalize_frames, create_folder, create_normalization_folders
from data import processed_data_folder_paths

# Main function to split and normilize the data
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

    # Three arrays to save to the frames after they been normilized
    normalized_frames_train = []
    normalized_frames_test = []
    normalized_frames_val = []

    train_folder, test_folder, val_folder = create_normalization_folders()

    # Three for loop to normilize train, test and, validation datasets
    for video_path in train_df['video_path']:
        print(f"Starting to normalize {video_path} ...")
        # Get video name
        video_name = Path(video_path).stem
        video_name = train_folder + '/' + video_name
        normalized_frames_train = normalize_frames(video_path)
        np.save(f"{video_name}.npy", normalized_frames_train)
    
    for video_path in test_df['video_path']:
        print(f"Starting to normalize {video_path} ...")
        # Get video name
        video_name = Path(video_path).stem
        video_name = test_folder + '/' + video_name
        normalized_frames_test = normalize_frames(video_path)
        np.save(f"{test_folder}.npy", normalized_frames_test)

    for video_path in val_df['video_path']:
        print(f"Starting to normalize {video_path} ...")
        # Get video name
        video_name = Path(video_path).stem
        video_name = val_folder + '/' + video_name
        normalized_frames_val = normalize_frames(video_path)
        np.save(f"{val_folder}.npy", normalized_frames_val)

if __name__ == '__main__':
    main()






