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

NUM_VALUES = 1000

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

# This function is used to trim\pad audio files to a specific (seconds * sampling frequency[fs]) seconds length
# Ideal average time is 5 seconds, the audio was sampled at 22050 Hz, so target length is 110250
def trim_audio(audio, seconds, fs):
    target_length = seconds * fs
    target_length = int(target_length)
    if len(audio) > target_length:
        audio = audio[:target_length]
    elif len(audio) < target_length:
        audio = np.pad(audio, (0, target_length - len(audio)), 'constant')
    return audio


def compute_mfcc(audio, sr):
    return librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=100)

# Navigate to the generated audio folder and extract the files
print("curdir:", os.curdir)
folder_path_generated = ".\\.\\Datasets\\WaveFake_GeneratedAudio\\generated_audio\\common_voices_prompts_from_conformer_fastspeech2_pwg_ljspeech"
file_list = os.listdir(folder_path_generated)
generated_audio_files = [file for file in file_list if file.endswith(".wav") or file.endswith(".mp3")]

# Navigate to the real audio folder and extract the files
folder_path_real = ".\\.\\Datasets\\LJSpeech_RealAudio\\LJSpeech-1.1\\wavs"
file_list = os.listdir(folder_path_real)
real_audio_files = [file for file in file_list if file.endswith(".wav") or file.endswith(".mp3")]


# First half is generated, second is real
sampleNamesGenerated = generated_audio_files[:NUM_VALUES]
sampleNamesReal = real_audio_files[:NUM_VALUES]

#Generate labels for the audio files
labels = [0] * len(sampleNamesGenerated) + [1] * len(sampleNamesReal)

# Initialize the arrays to store the bispectrum, bicoherence and MFCCs
bispectrum = []
bicoherence = []
mfcc = []
ffts = []
audio_files = []

# Convert generated samples to mono
for file in sampleNamesGenerated:
    file_path = os.path.join(folder_path_generated, file)
    audio, fs = sf.read(file_path)
    if audio.ndim > 1:
        audio = audio.mean(axis=1)  # Take the average of the channels to convert to mono
    audio = trim_audio(audio, 3.5, fs)
    ffts.append(abs(fft.fft(audio)))
    audio_files.append(audio)

# Convert real samples to mono
for file in sampleNamesReal:
    file_path = os.path.join(folder_path_real, file)
    audio, fs = sf.read(file_path)
    if audio.ndim > 1:
        audio = audio.mean(axis=1)  # Take the average of the channels to convert to mono
    audio = trim_audio(audio, 3.5, fs)
    ffts.append(abs(fft.fft(audio)))
    audio_files.append(audio)

print("Sampling frequency: " + str(fs) + "Hz")
    
# Compute bispectrum for all the samples, each bispectrum variable contains N number of samples, each sample is represented as an
# array of the bispectrum values
#bispectrum = compute_bispectrum(audio_files)

# Calculate amplitude spectrum for the signals
#amplitude_spectrum = calculate_amplitude_spectrum(audio_files)

# Compute the bicoherence of the generated samples
#bicoherence = calculate_bicoherence(bispectrum, amplitude_spectrum)

#print("bicoh shape:", bicoherence[0].shape)

# Compute MFCCs for the samples
mfcc = [ compute_mfcc(audio, fs) for audio in audio_files]

# Reshape the MFCCs to a 2D array
print(len(mfcc))
print(len(mfcc[0]))
print(len(mfcc[0][0]))

mfcc = np.array(mfcc)
mfcc = mfcc.reshape(NUM_VALUES*2, 15100)

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
np.save("feature_set.npy", feature_set)
np.save("labels.npy", labels)

random_array = np.random.randint(-1000, 1001, size=(40, 100000))

np.save("random_array.npy", random_array)
np.save("test.npy", random_array)