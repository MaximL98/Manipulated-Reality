'''
    This code was used to trim silence from the Fluent Speech Corpus dataset.
    The Fluent Speech Corpus dataset was downloaded from the Fluent Speech Commands dataset.
    It is a dataset of spoken commands in English.
'''

# import librosa
# import soundfile as sf
# import os

# # Assign directory
# directory = r"Manipulated-Reality\\Datasets\\FluentSpeechCorpus_dataset\\archive\\fluent_speech_commands_dataset\\wavs\\speakers"
 
# # Iterate over folders in speakers database directory
# for foldername in os.listdir(directory):
#     # For each speaker, iterate over their audio recordings and trim them
#     for filename in os.listdir(directory + "\\" + foldername):
#         # Load the audio file
#         waveform, sample_rate = librosa.load(directory + "\\" + foldername + "\\" + filename)
        
#         # Trim the audio
#         trimmed_waveform = librosa.effects.trim(waveform, top_db=30)[0]
        
#         # Write the trimmed audio to a new file
#         sf.write("Manipulated-Reality\\Datasets\\FluentSpeechCorpus(Trimmed)_dataset\\" + filename, trimmed_waveform, sample_rate)
 
