import os
import soundfile as sf
import numpy as np
from scipy import fftpack, fft
import librosa
import keras

ffts = []
audio_files = []
NUM_MFCC = 100

# This function takes an audio file and returns an array with chunks of 1 second
# If a file is 5.75 seconds, it returns an array of size 6 with the last index padded with 0's
def trim_audio(audio, fs):
    chunks = [audio[x:x + 1000] for x in range(0, len(audio), 1000)]
    if (len(chunks[-1]) > 750):
        # Pad chunks longer than 750 numbers with 0's
        chunks[-1] = np.pad(chunks[-1], (0, 1000 - len(chunks[-1])), 'constant')
    else :
      chunks = chunks[:-1]
   
    return chunks

def compute_mfcc(audio, sr, num_mfcc):
    return librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=num_mfcc)


path_to_audio = "Test_audio_MR.mp3"
# Convert generated samples to mono
audio, fs = sf.read(path_to_audio)
if audio.ndim > 1:
    audio = audio.mean(axis=1)  # Take the average of the channels to convert to mono
audio_chunk = trim_audio(audio, fs)
for audio in audio_chunk:
    ffts.append(abs(fft.fft(audio)))
    audio_files.append(audio)
    
number_of_generated_samples = len(audio_chunk)

print(len(audio_files))
mfcc = compute_mfcc(audio, fs, NUM_MFCC)
mfcc = np.array(mfcc)
mfcc = mfcc.reshape(len(audio_files), NUM_MFCC*2)

# Perform delta cepstral and delta^2 analysis on the mfcc_bicoherence array
delta_mfcc_bicoherence = librosa.feature.delta(mfcc)
delta2_mfcc_bicoherence = librosa.feature.delta(mfcc, order=2)

features_vector = np.concatenate((mfcc, delta_mfcc_bicoherence, delta2_mfcc_bicoherence), axis=1)

model = keras.saving.load_model("TheAudioModel.keras")

print(features_vector.shape)

print(model.predict(features_vector))

print("done")