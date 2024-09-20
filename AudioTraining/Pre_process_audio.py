import os
from scipy import fft
# Used for bi-coherence analysis
import soundfile as sf
import numpy as np
# Used for MFCC analysis
import librosa

''' This code is used to perform pre-processing on entire folders of audio files. 
    To perform pre-processing simply choose the index of the first and the last file in the folder.
    The code will extract the audio files, convert them to mono, resample them to a target frequency, split them into chunks, compute the MFCCs, 
    delta cepstral and delta^2 analysis and save the features to a numpy file.
    
    NOTE: Each audio file is split into chunks to make CNN input easier.
    YOU decide what is the length of each audio sample.
    YOU decide how many MFCC features will be extracted from each chunk of audio. 
    YOU decide on the target frequency of the files.
    
    IMPORTANT: MFCCs ARE NOT 1 DIMENSIONAL, THEY ARE 2D ARRAYS. During the initial phase of the project, each MFCC coefficient yielded 44 depepdencies as a list. 
    i.e. an array of 100 MFCCs yielded 4400 features.
    
    HOW TO USE: Simply choose the folder path of the audio files using the global variables below.
    Choose the start and end index of the files you want to process.
    Choose the number of MFCCs you want to extract.
    Choose the target frequency of the audio files.
    Choose the length of each audio sample.
    Choose the name of the database.
    Choose whether you want to preprocess real and/or generated audio files.
    
    Don't worry, the output file name contains all of the important information about the extraction process.
    For example: [0-3106_(REAL)_0-16283_(FAKE)_1000ms_for_sample_22050hz_frequency_WaveFake_dataset_labels_set.npy]
'''

REAL_START_INDEX = 0
REAL_END_INDEX = 200000
GENERATED_START_INDEX = 0
GENERATED_END_INDEX = 200000
NUM_MFCC = 100
TARGET_FREQUENCY = 22050 # Hz
LENGTH_OF_EACH_SAMPLE = 1 # In seconds

# Path to the folders containing the audio files
GENERATED_AUDIO_DIRECTORY = "Path\To\Your\Generated\Audio\Files"
REAL_AUDIO_DIRECTORY = "Path\To\Your\Real\Audio\Files"

DATABASE_NAME = "FluentSpeechCorpus" # Name the output file with the database name

useReal = True
useFake = False

# ######################################################################################################
# ######################################## In-The-Wild dataset #########################################
# ######################################################################################################

# folder_path_generated = "Manipulated-Reality\\Datasets\\InTheWild_dataset\\release_in_the_wild"
# folder_path_real = "Manipulated-Reality\\Datasets\\InTheWild_dataset\\release_in_the_wild"
# DATABASE_NAME = "InTheWild_dataset"
# GENERATED_AUDIO_DIRECTORY = "Manipulated-Reality\\Datasets\\InTheWild_dataset\\release_in_the_wild"
# REAL_AUDIO_DIRECTORY = "Manipulated-Reality\\Datasets\\InTheWild_dataset\\release_in_the_wild"
# useReal = True
# useFake = False

# # Read CSV fileclear
# data = pd.read_csv("InTheWild_Labels.csv")
# data = data[START_INDEX:END_INDEX if END_INDEX < len(data) else len(data)]

# generated_audio_files = data[(data['label'] == 'spoof')]
# real_audio_files = data[(data['label'] == 'bona-fide')]

# generated_audio_files = generated_audio_files['file']
# real_audio_files = real_audio_files['file']

# ######################################################################################################
# ######################################################################################################
# ######################################################################################################

# This function takes an audio file and returns an array with chunks of 1 second
# If a file is 5.75 seconds, it returns an array of size 6 with the last index padded with 0's
def trim_audio(audio, fs):
    len_of_each_sample = fs * LENGTH_OF_EACH_SAMPLE
    chunks = [audio[x:x + int(len_of_each_sample)] for x in range(0, len(audio), int(len_of_each_sample))]
    if (len(chunks[-1]) > fs*0.75):
        # Pad chunks longer than 75% of a second with 0's
        chunks[-1] = np.pad(chunks[-1], (0, int(len_of_each_sample) - len(chunks[-1])), 'constant')
    else :
      chunks = chunks[:-1]
   
    return chunks

# This function is used to compute the MFCCs of the audio files
def compute_mfcc(audio, sr, num_mfcc):
    return librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=num_mfcc)


# If useFake is true, navigate to the generated audio folder and extract the files
if useFake:
    folder_path_generated = GENERATED_AUDIO_DIRECTORY
    file_list = os.listdir(folder_path_generated)
    generated_audio_files = [file for file in file_list if file.endswith(".wav") or file.endswith(".mp3")]
else:
    generated_audio_files = []

# If useReal is true, navigate to the real audio folder and extract the files
if useReal:
    # Navigate to the real audio folder and extract the files
    folder_path_real = REAL_AUDIO_DIRECTORY
    file_list = os.listdir(folder_path_real)
    real_audio_files = [file for file in file_list if file.endswith(".wav") or file.endswith(".mp3")]
else:
    real_audio_files = []


# This part makes sure that if a number of samples greater than the number of files in the folder is requested, the code will not crash
sampleNamesGenerated = generated_audio_files[GENERATED_START_INDEX:(len(generated_audio_files) if GENERATED_END_INDEX > len(generated_audio_files) else GENERATED_END_INDEX)]
sampleNamesReal = real_audio_files[REAL_START_INDEX:len(real_audio_files) if REAL_END_INDEX > len(real_audio_files) else REAL_END_INDEX]

print("Number of generated samples: " + str(len(sampleNamesGenerated)))
print("Number of real samples: " + str(len(sampleNamesReal)))


# Initialize the arrays to store the bispectrum, bicoherence and MFCCs
bispectrum = []
bicoherence = []
mfcc = []
ffts = []
audio_files = []
number_of_real_samples = 0
number_of_generated_samples = 0

# Convert generated samples to mono
for file in sampleNamesGenerated:
    file_path = os.path.join(folder_path_generated, file)
    audio, fs = sf.read(file_path)
    if audio.ndim > 1:
        audio = audio.mean(axis=1)  # Take the average of the channels to convert to mono
    # Split audio into 1 second chunks
    audio_chunk = trim_audio(audio, fs)
    for audio in audio_chunk:
        ffts.append(abs(fft.fft(audio)))
        # Resample each audio file to TARGET_FREQUENCY
        audio = librosa.resample(audio, orig_sr=fs, target_sr=TARGET_FREQUENCY, res_type='soxr_vhq')
        audio_files.append(audio)
    number_of_generated_samples += len(audio_chunk)



# Convert real samples to mono
for file in sampleNamesReal:
    file_path = os.path.join(folder_path_real, file)
    audio, fs = sf.read(file_path)
    if audio.ndim > 1:
        audio = audio.mean(axis=1)  # Take the average of the channels to convert to mono
    # Split audio into 1 second chunks    
    audio_chunk = trim_audio(audio, fs)
    for audio in audio_chunk:
        ffts.append(abs(fft.fft(audio)))
        # Resample each audio file to 44100Hz
        audio = librosa.resample(audio, orig_sr=fs, target_sr=TARGET_FREQUENCY, res_type='soxr_vhq')
        audio_files.append(audio)
    number_of_real_samples += len(audio_chunk)


print("Sampling frequency: " + str(fs) + "Hz")
    
#Generate labels for the audio files
labels = [0] * number_of_generated_samples + [1] * number_of_real_samples

# Compute MFCCs for the samples, each audio converts into a 2D array of MFCCs with dimension [100][2] (2 coefficients per each index)
mfcc = [ compute_mfcc(audio, fs, NUM_MFCC) for audio in audio_files]

# Reshape the MFCCs to a 2D array
mfcc = np.array(mfcc)
mfcc = mfcc.reshape(len(audio_files), NUM_MFCC*len(mfcc[0][0]))

# Convert complex numbers to real numbers by taking the absolute value
#bicoherence_abs = np.abs(bicoherence)

# Concatenate the bicoherence and MFCC arrays
print("mfcc_generated shape:", len(mfcc), len(mfcc[0]))


# Perform delta cepstral and delta^2 analysis on the mfcc array
delta_mfcc = librosa.feature.delta(mfcc)
delta2_mfcc = librosa.feature.delta(mfcc, order=2)

# Concatenate the MFCCs, delta cepstral and delta^2 arrays into a single feature set [MFCC, delta, delta^2]
feature_set = np.concatenate((mfcc,delta_mfcc, delta2_mfcc), axis=1)


print("Feature_set shape:", len(feature_set), len(feature_set[0]))

# Save the feature set and labels to a file
if DATABASE_NAME == "InTheWild_dataset":
    feature_set_name = str(REAL_START_INDEX) + "-" + str(len(sampleNamesReal)) + "_samples_" +  str(int(LENGTH_OF_EACH_SAMPLE*1000)) + "ms_for_sample_" + str(int(TARGET_FREQUENCY)) + "hz_frequency_" + DATABASE_NAME + "_feature_set.npy"
    labels_name = str(REAL_START_INDEX) + "-" + str(len(sampleNamesReal)) + "_samples_" + str(int(LENGTH_OF_EACH_SAMPLE*1000)) + "ms_for_sample_" + str(int(TARGET_FREQUENCY)) + "hz_frequency_" + DATABASE_NAME + "_labels_set.npy"
else :
    feature_set_name = str(REAL_START_INDEX) + "-" + str(len(sampleNamesReal)) + "_(REAL)_" + str(GENERATED_START_INDEX) + "-" + str(len(sampleNamesGenerated)) + "_(FAKE)_" + str(int(LENGTH_OF_EACH_SAMPLE*1000)) + "ms_for_sample_" + str(int(TARGET_FREQUENCY)) + "hz_frequency_" + DATABASE_NAME + "_feature_set.npy"
    labels_name = str(REAL_START_INDEX) + "-" + str(len(sampleNamesReal)) + "_(REAL)_" + str(GENERATED_START_INDEX) + "-" + str(len(sampleNamesGenerated)) + "_(FAKE)_" + str(int(LENGTH_OF_EACH_SAMPLE*1000)) + "ms_for_sample_" + str(int(TARGET_FREQUENCY)) + "hz_frequency_" + DATABASE_NAME + "_labels_set.npy"
 
# Save the feature set and labels to a numpy file
np.save(os.path.join("Audio_numpy_files\\", feature_set_name), feature_set)
np.save(os.path.join("Audio_numpy_files\\", labels_name), labels)

print("Created", feature_set_name)
print("Created", labels_name)



############################### This code is not currently used but might be used in future for further database pre-processing analysis ###############################


# # Used for bi-coherence analysis
# import scipy.signal as signal
# import pandas as pd
# from scipy import fftpack

# Compute bispectrum for all the samples, each bispectrum variable contains N number of samples, each sample is represented as an
# array of the bispectrum values
#bispectrum = compute_bispectrum(audio_files)

# Calculate amplitude spectrum for the signals
#amplitude_spectrum = calculate_amplitude_spectrum(audio_files)

# Compute the bicoherence of the generated samples
#bicoherence = calculate_bicoherence(bispectrum, amplitude_spectrum)


# # This function is used to calculate the bispectrum of the signals
# def compute_bispectrum(samples):
#     bispectrum = []
#     for sample in samples:
#         # Compute the Fourier Transform of the signal
#         F = np.fft.fft(sample)
#         # Compute the Fourier Transform of the conjugate of the signal
#         F_star = np.conj(F)
#         # Compute the bispectrum using the convolution theorem
#         bispectrum.append(F * F_star * np.roll(F,  1))
#     return bispectrum
        
# # This function is used to calculate the bicoherence of the signals
# def calculate_bicoherence(bispectrums, amplitude_spectrum):
#     bicoherence = []
#     # Normalize the bispectrum
#     for i, bispectrum in enumerate(bispectrums):
#         normalized_bispectrum = bispectrum / (amplitude_spectrum[i]**2 +  1e-10)  # Adding a small constant for numerical stability
#         bicoherence.append(normalized_bispectrum)
#     return bicoherence

# # This function is used to calculate the amplitude spectrum of the signals
# # The amplitude spectrum is a square representation of the fourier transform of a signal
# def calculate_amplitude_spectrum(signals):
#     amplitude_spectrum = []
#     for signal in signals:
#         amplitude_spectrum.append(np.abs(fft.fft(signal))**2)
#     return amplitude_spectrum