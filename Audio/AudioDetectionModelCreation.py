import os
from AudioFunctions import function_collection

# Used for bi-coherence analysis
import scipy.signal as signal
from scipy import fftpack, fft

# Used for bi-coherence analysis
import soundfile as sf
import numpy as np


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
    if len(audio) > target_length:
        audio = audio[:target_length]
    elif len(audio) < target_length:
        audio = np.pad(audio, (0, target_length - len(audio)), 'constant')
    return audio


# Navigate to the generated audio folder and extract the files
folder_path_generated = ".\\.\\Datasets\\WaveFake_GeneratedAudio\\generated_audio\\common_voices_prompts_from_conformer_fastspeech2_pwg_ljspeech"
file_list = os.listdir(folder_path_generated)
generated_audio_files = [file for file in file_list if file.endswith(".wav") or file.endswith(".mp3")]

# Navigate to the real audio folder and extract the files
folder_path_real = ".\\.\\Datasets\\LJSpeech_RealAudio\\LJSpeech-1.1\\wavs"
file_list = os.listdir(folder_path_real)
real_audio_files = [file for file in file_list if file.endswith(".wav") or file.endswith(".mp3")]

generated_samples_20 = generated_audio_files[:2000]
real_samples_20 = real_audio_files[:2000]

print("Generated Audio Files: ", len(generated_samples_20))  
print("Real Audio Files: ", len(real_samples_20))

FFTs_generated = []
FFTs_real = []
generated_audio_files = []
real_audio_files = []

# Convert generated samples to mono
for file in generated_samples_20:
    file_path = os.path.join(folder_path_generated, file)
    audio, fs = sf.read(file_path)
    if audio.ndim > 1:
        audio = audio.mean(axis=1)  # Take the average of the channels to convert to mono
    audio = trim_audio(audio, 5, fs)
    FFTs_generated.append(abs(fft.fft(audio)))
    generated_audio_files.append(audio)

# Convert real samples to mono
for file in real_samples_20:
    file_path = os.path.join(folder_path_real, file)
    audio, fs = sf.read(file_path)
    if audio.ndim > 1:
        audio = audio.mean(axis=1)  # Take the average of the channels to convert to mono
    audio = trim_audio(audio, 5, fs)
    FFTs_real.append(abs(fft.fft(audio)))
    real_audio_files.append(audio)
    
print("Sampling frequency: " + str(fs) + "Hz")
    
# Compute bispectrum for all the samples, each bispectrum variable contains N number of samples, each sample is represented as an
# array of the bispectrum values
bispectrum_generated = compute_bispectrum(generated_audio_files)
bispectrum_real = compute_bispectrum(real_audio_files)

# Calculate amplitude spectrum for the signals
amplitude_spectrum_generated = calculate_amplitude_spectrum(generated_audio_files)
amplitude_spectrum_real = calculate_amplitude_spectrum(real_audio_files)

# Compute the bicoherence of the generated samples
bicoh_generated = calculate_bicoherence(bispectrum_generated, amplitude_spectrum_generated)

# Compute the bicoherence of the real samples2
bicoh_real = calculate_bicoherence(bispectrum_real, amplitude_spectrum_generated)

# Print the length of the bicoherence list for generated samples
print("Bicoherence generated size:" + str(len(bicoh_generated)))

# Print the length of the bicoherence list for real samples
print("Bicoherence real size:" + str(len(bicoh_real)))