from moviepy.editor import VideoFileClip


# This function gets a video file path and extracts from it a audio file.
def extract_audio(video_file_path, audio_file_path = None):
    try:
        # Check if user gave a specific path he wants the audio file to be saved at
        # If not, use basic path
        if not audio_file_path:
            # This is the path to where we are saving the audio extracted from the video
            audio_file_path = 'DeepFake_audio_only.mp3'

        # Load the video
        video = VideoFileClip(video_file_path)

        # Extract the audio
        audio_only = video.audio

        if audio_only:
            # Write the audio in the audio file
            audio_only.write_audiofile(audio_file_path)
        else:
            print("This video does not contain audio!")
            return None

        # Close the video and the audio
        audio_only.close()
        video.close()
        print("Audio extraction was successful!")
        return video_file_path, audio_file_path
    except Exception as e:
        print("An Error occurred: ", e)
        return None
