from sklearn.discriminant_analysis import StandardScaler
import soundfile as sf
import numpy as np
import numpy as np
import tensorflow as tf # tested with 1.14.0
import keras
from keras import models
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
import os
import librosa
import Feature_Extraction_from_sample as feature_extraction
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, RobustScaler

SAMPLE_FREQUENCY = 22050


###########################################
array_of_feature_set_names = [
                              "5_10_percent_1000ms_22050hz\\0-1500_(REAL)_0-1500_(FAKE)_1000ms_for_sample_WaveFake_dataset_feature_set.npy"

]

array_of_labels_set_names = [
                              "5_10_percent_1000ms_22050hz\\0-1500_(REAL)_0-1500_(FAKE)_1000ms_for_sample_WaveFake_dataset_labels_set.npy"

]
class_names = ["fake", "real"]

train_data = []
for dataset_features_name in array_of_feature_set_names:
    destination_dataset = 'Audio_numpy_files\\' + dataset_features_name
    print(destination_dataset)
    train_data.append(np.load(destination_dataset))

train_data = np.concatenate(train_data, axis=0)

labels = []
for dataset_labels_name in array_of_labels_set_names:
    destination_dataset = 'Audio_numpy_files\\' + dataset_labels_name
    print(destination_dataset)
    labels.append(np.load(destination_dataset))

labels = np.concatenate(labels, axis=0)
labels = labels.astype('int32')

print(labels.shape)


print(train_data.dtype)
print(labels.dtype)
print(train_data[0][0].dtype)


# scaler = MinMaxScaler((-1, 1))
# train_data = scaler.fit_transform(train_data)


x_train, x_test, y_train, y_test = train_test_split(train_data, labels, test_size=0.25, random_state=123)
x_train, x_val, y_train, y_val = train_test_split(x_train, y_train, test_size=0.25, random_state=123)

###########################################
LENGTH_OF_EACH_SAMPLE = 1
TARGET_SAMPLE_RATE = 22050

def predictAudioFile(model, list):
    return model.predict(list)

model = models.load_model('1_Audio_model.keras')

import pickle

with open('scaler.pkl', 'rb') as file:
    scaler = pickle.load(file)
    
threshold = 0.5

print("****************************************************************")
print("FAKE")
print("****************************************************************")


test = scaler.fit_transform(feature_extraction.audio_file_feature_extractor('audio-file-fake-test.mp3', 100, 22050, 1))
test1= test
prediction = predictAudioFile(model, test)
predicted = (prediction >= threshold).astype("int32")

counter = 0
for i in range(len(prediction)):
    if prediction[i] >= threshold:
        counter += 1
print("Data size: ", len(prediction),"Counter = ", counter, )

for i in range(9):
    print(prediction[i], " label: fake", f"predicted: {predicted[i]}")

print("****************************************************************")
print("REAL")
print("****************************************************************")

test = scaler.fit_transform(feature_extraction.audio_file_feature_extractor('audio-file-real-test.mp3', 100, 22050, 1))
test2= test
prediction = predictAudioFile(model, test)
predicted = (prediction >= threshold).astype("int32")

counter = 0
for i in range(len(prediction)):
    if prediction[i] >= threshold:
        counter += 1
print("Data size: ", len(prediction),"Counter = ", counter)

for i in range(15):
    print(prediction[i], " label: real", f"predicted: {predicted[i]}")

print("****************************************************************")
print("REAL 2")
print("****************************************************************")

test = scaler.fit_transform(feature_extraction.audio_file_feature_extractor('Dima_recording_real.mp3', 100, SAMPLE_FREQUENCY, 1))
test2= test
prediction = predictAudioFile(model, test)
predicted = (prediction >= threshold).astype("int32")

counter = 0
for i in range(len(prediction)):
    if prediction[i] >= threshold:
        counter += 1
print("Data size: ", len(prediction),"Counter = ", counter)

for i in range(3):
    print(prediction[i], " label: real", f"predicted: {predicted[i]}")

print("****************************************************************")
print("TEST")
print("****************************************************************")
prediction = predictAudioFile(model, scaler.fit_transform(x_test))
predicted = (prediction >= threshold).astype("int32")

counter = 0
counter_label_correct = 0
for i in range(len(prediction)):
    if prediction[i] > threshold and y_test[i] == 0:
        counter += 1
    if predicted[i] == y_test[i]:
        counter_label_correct += 1
print("Data size: ", len(prediction),"Counter = ", counter, f"Counter label correct: {counter_label_correct}")

for i in range(15):
    print(prediction[i], " label:", y_test[i], f"predicted: {predicted[i]}")
    
print("****************************************************************")
print("****************************************************************")
print("****************************************************************")
    
print("****************************************************************")
print("xtest[0]: ", x_test[0], f"label: {y_test[0]}", f"predicted: {predicted[i]}")
print("fake:", test1)
print("real", test2)


