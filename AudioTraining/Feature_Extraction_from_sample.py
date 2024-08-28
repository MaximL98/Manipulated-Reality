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

def audio_file_feature_extractor(audioFilePath, NUM_MFCC = 100, TARGET_FREQUENCY = 22050, LENGTH_OF_EACH_SAMPLE = 1):
    """
    This function extracts features from audio files, input can be a single file or a list of files. The function extracts features from each file and returns a list of features.
    Every audio file lower than 75% of the LENGTH_OF_EACH_SAMPLE will be DISCARDED. Every audio file higher than 75% of the LENGTH_OF_EACH_SAMPLE will be padded with 0's.
    
    example: 
    Input is a list of two files [file1.wav 3.78 seconds, file2.mp3 0.98 seconds], output list is [[file1_second1_features, file1_second2_features, file1_second3_features, file1_second4_features], [file2_second1_features]].
    
    Input:
    audioFiles: A list of audio files to extract features from.
    NUM_MFCC: Number of MFCC features to extract.
    TARGET_FREQUENCY: The target frequency to resample the audio files to (The higher the frequency, the more time it will take to extract the features).
    LENGTH_OF_EACH_SAMPLE: The length of each sample in seconds.
    
    Output:
    extracted_features: A list of extracted features. Eeach index indicates a file, there can be a list in each index if the audio sample is bigger than LENGTH_OF_EACH_SAMPLE.
    """
    audio_files = []
    number_of_generated_samples = 0
    # Convert generated samples to mono
    audio, sample_frequency = sf.read(audioFilePath)
    if audio.ndim > 1:
        audio = audio.mean(axis=1)  # Take the average of the channels to convert to mono
    # Split audio into 1 second chunks
    audio_chunks = trim_audio(audio, sample_frequency, LENGTH_OF_EACH_SAMPLE)
        
    chunks = []
    for audio in audio_chunks:
        # Resample each audio file to TARGET_FREQUENCY
        audio = librosa.resample(audio, orig_sr=sample_frequency, target_sr=TARGET_FREQUENCY, res_type='soxr_vhq')
        chunks.append(audio)
        number_of_generated_samples += len(audio_chunks)    
         
    mfcc = [ compute_mfcc(audio, sample_frequency, NUM_MFCC) for audio in chunks]
    mfcc = np.array(mfcc)
    mfcc = mfcc.reshape(len(chunks), NUM_MFCC*len(mfcc[0][0]))
    # Perform delta cepstral and delta^2 analysis on the mfcc_bicoherence array
    delta_mfcc_bicoherence = librosa.feature.delta(mfcc)
    delta2_mfcc_bicoherence = librosa.feature.delta(mfcc, order=2)
    feature_set = np.concatenate((mfcc,delta_mfcc_bicoherence, delta2_mfcc_bicoherence), axis=1)
    
    return feature_set    
    

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
def trim_audio(audio, fs, length_of_each_sample = 1):
    len_of_each_sample = fs * length_of_each_sample
    chunks = [audio[x:x + int(len_of_each_sample)] for x in range(0, len(audio), int(len_of_each_sample))]
    if (len(chunks[-1]) > fs*0.75):
        # Pad chunks longer than 75% of a second with 0's
        chunks[-1] = np.pad(chunks[-1], (0, int(len_of_each_sample) - len(chunks[-1])), 'constant')
    else :
      chunks = chunks[:-1]
   
    return chunks


def compute_mfcc(audio, sr, num_mfcc):
    return librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=num_mfcc)
