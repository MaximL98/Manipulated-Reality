import os
# from AudioFunctions import function_collection

# Used for bi-coherence analysis
import scipy.signal as signal
from scipy import fftpack, fft

# Used for bi-coherence analysis
import soundfile as sf
import numpy as np

# Used for MFCC analysis
import librosa

from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import pandas as pd

REAL_START_INDEX = 0
REAL_END_INDEX = 200000
GENERATED_START_INDEX = 0
GENERATED_END_INDEX = 200000
NUM_MFCC = 100
TARGET_FREQUENCY = 22050
LENGTH_OF_EACH_SAMPLE = 1

# GENERATED_AUDIO_DIRECTORY = "Manipulated-Reality\\Datasets\\WaveFake_dataset\\generated_audio\\common_voices_prompts_from_conformer_fastspeech2_pwg_ljspeech"
# REAL_AUDIO_DIRECTORY = "Manipulated-Reality\\Datasets\\WaveFake_dataset\\real_audio"    
# DATABASE_NAME = "WaveFake_dataset"
# useReal = True
# useFalse = True


# GENERATED_AUDIO_DIRECTORY = "Manipulated-Reality\Datasets\DeepVoice_dataset\FAKE"
# REAL_AUDIO_DIRECTORY = "Manipulated-Reality\Datasets\DeepVoice_dataset\REAL"
# DATABASE_NAME = "DeepVoice_dataset"
# useReal = True
# useFalse = True


GENERATED_AUDIO_DIRECTORY = "Manipulated-Reality\Datasets\FluentSpeechCorpus(Trimmed)_dataset"
REAL_AUDIO_DIRECTORY = "Manipulated-Reality\Datasets\FluentSpeechCorpus(Trimmed)_dataset"
DATABASE_NAME = "FluentSpeechCorpus"
useReal = True
useFalse = False


# GENERATED_AUDIO_DIRECTORY = "Audio_numpy_files\\test\\real"
# REAL_AUDIO_DIRECTORY = "Audio_numpy_files\\test\\fake"    
# DATABASE_NAME = "test_dataset"

# ######################################################################################################
# ######################################## In-The-Wild dataset #########################################
# ######################################################################################################

# folder_path_generated = "Manipulated-Reality\\Datasets\\InTheWild_dataset\\release_in_the_wild"
# folder_path_real = "Manipulated-Reality\\Datasets\\InTheWild_dataset\\release_in_the_wild"
# DATABASE_NAME = "InTheWild_dataset"
# GENERATED_AUDIO_DIRECTORY = "Manipulated-Reality\\Datasets\\InTheWild_dataset\\release_in_the_wild"
# REAL_AUDIO_DIRECTORY = "Manipulated-Reality\\Datasets\\InTheWild_dataset\\release_in_the_wild"
# useReal = True
# useFalse = False

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


# This function is used to calculate the bispectrum of the signals
def compute_bispectrum(samples):
    bispectrum = []
    for sample in samples:
        # Compute the Fourier Transform of the signal
        F = np.fft.fft(sample)
        # Compute the Fourier Transform of the conjugate of the signal
        F_star = np.conj(F)
        # Compute the bispectrum using the convolution theorem
        bispectrum.append(F * F_star * np.roll(F,  1))
    return bispectrum
        
# This function is used to calculate the bicoherence of the signals
def calculate_bicoherence(bispectrums, amplitude_spectrum):
    bicoherence = []
    # Normalize the bispectrum
    for i, bispectrum in enumerate(bispectrums):
        normalized_bispectrum = bispectrum / (amplitude_spectrum[i]**2 +  1e-10)  # Adding a small constant for numerical stability
        bicoherence.append(normalized_bispectrum)
    return bicoherence

# This function is used to calculate the amplitude spectrum of the signals
# The amplitude spectrum is a square representation of the fourier transform of a signal
def calculate_amplitude_spectrum(signals):
    amplitude_spectrum = []
    for signal in signals:
        amplitude_spectrum.append(np.abs(fft.fft(signal))**2)
    return amplitude_spectrum

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


def compute_mfcc(audio, sr, num_mfcc):
    return librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=num_mfcc)

# Navigate to the generated audio folder and extract the files
print("curdir:", os.listdir("."))

if useFalse:
    folder_path_generated = GENERATED_AUDIO_DIRECTORY
    file_list = os.listdir(folder_path_generated)
    generated_audio_files = [file for file in file_list if file.endswith(".wav") or file.endswith(".mp3")]
else:
    generated_audio_files = []

if useReal:
    # Navigate to the real audio folder and extract the files
    folder_path_real = REAL_AUDIO_DIRECTORY
    file_list = os.listdir(folder_path_real)
    real_audio_files = [file for file in file_list if file.endswith(".wav") or file.endswith(".mp3")]
else:
    real_audio_files = []



# Continue with the rest of the code...
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
    
# Compute bispectrum for all the samples, each bispectrum variable contains N number of samples, each sample is represented as an
# array of the bispectrum values
#bispectrum = compute_bispectrum(audio_files)

# Calculate amplitude spectrum for the signals
#amplitude_spectrum = calculate_amplitude_spectrum(audio_files)

# Compute the bicoherence of the generated samples
#bicoherence = calculate_bicoherence(bispectrum, amplitude_spectrum)

#print("bicoh shape:", bicoherence[0].shape)

#Generate labels for the audio files
labels = [0] * number_of_generated_samples + [1] * number_of_real_samples


# Compute MFCCs for the samples, each audio converts into a 2D array of MFCCs with dimension [100][2] (2 coefficients per each index)
mfcc = [ compute_mfcc(audio, fs, NUM_MFCC) for audio in audio_files]

# Reshape the MFCCs to a 2D array
print(len(labels))
print(len(audio_files))
print(len(mfcc))
print(len(mfcc[0]))
print(len(mfcc[0][0]))


mfcc = np.array(mfcc)
mfcc = mfcc.reshape(len(audio_files), NUM_MFCC*len(mfcc[0][0]))

# Convert complex numbers to real numbers by taking the absolute value
#bicoherence_abs = np.abs(bicoherence)

# Concatenate the bicoherence and MFCC arrays
print("mfcc_generated shape:", len(mfcc), len(mfcc[0]))


# Perform delta cepstral and delta^2 analysis on the mfcc_bicoherence array
delta_mfcc_bicoherence = librosa.feature.delta(mfcc)
delta2_mfcc_bicoherence = librosa.feature.delta(mfcc, order=2)

print("delta_mfcc_bicoherence shape:", len(delta_mfcc_bicoherence))
print("delta_mfcc_bicoherence shape:", len(delta_mfcc_bicoherence[0]))
print("delta2_mfcc_bicoherence shape:", len(delta2_mfcc_bicoherence))
print("delta2_mfcc_bicoherence shape:", len(delta2_mfcc_bicoherence[0]))

# Concatenate the bicoherence, MFCC, delta cepstral, delta^2 cepstral arrays to create a complete feature set
#This is the most ideal one
#feature_set = np.concatenate((mfcc, bicoherence_abs,delta_mfcc_bicoherence, delta2_mfcc_bicoherence), axis=1)
#This is shorter and only includes features
feature_set = np.concatenate((mfcc,delta_mfcc_bicoherence, delta2_mfcc_bicoherence), axis=1)


print("feature_set shape:", len(feature_set), len(feature_set[0]))

# Save the feature set and labels to a file
if DATABASE_NAME == "InTheWild_dataset":
    feature_set_name = str(REAL_START_INDEX) + "-" + str(len(sampleNamesReal)) + "_samples_" +  str(int(LENGTH_OF_EACH_SAMPLE*1000)) + "ms_for_sample_" + str(int(TARGET_FREQUENCY)) + "hz_frequency_" + DATABASE_NAME + "_feature_set.npy"
    labels_name = str(REAL_START_INDEX) + "-" + str(len(sampleNamesReal)) + "_samples_" + str(int(LENGTH_OF_EACH_SAMPLE*1000)) + "ms_for_sample_" + str(int(TARGET_FREQUENCY)) + "hz_frequency_" + DATABASE_NAME + "_labels_set.npy"
else :
    feature_set_name = str(REAL_START_INDEX) + "-" + str(len(sampleNamesReal)) + "_(REAL)_" + str(GENERATED_START_INDEX) + "-" + str(len(sampleNamesGenerated)) + "_(FAKE)_" + str(int(LENGTH_OF_EACH_SAMPLE*1000)) + "ms_for_sample_" + str(int(TARGET_FREQUENCY)) + "hz_frequency_" + DATABASE_NAME + "_feature_set.npy"
    labels_name = str(REAL_START_INDEX) + "-" + str(len(sampleNamesReal)) + "_(REAL)_" + str(GENERATED_START_INDEX) + "-" + str(len(sampleNamesGenerated)) + "_(FAKE)_" + str(int(LENGTH_OF_EACH_SAMPLE*1000)) + "ms_for_sample_" + str(int(TARGET_FREQUENCY)) + "hz_frequency_" + DATABASE_NAME + "_labels_set.npy"
 

np.save(os.path.join("Audio_numpy_files\\", feature_set_name), feature_set)
np.save(os.path.join("Audio_numpy_files\\", labels_name), labels)

print("Created", feature_set_name)
print("Created", labels_name)