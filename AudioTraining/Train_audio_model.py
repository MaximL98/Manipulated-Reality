import os
import numpy as np
from sklearn.discriminant_analysis import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, RobustScaler
import tensorflow as tf # tested with 1.14.0
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
from sklearn.metrics import classification_report # tested with 0.21.2l
from tensorflow import keras
from keras import models
from keras import layers
# Supress deprecation warnings
import logging
logging.getLogger('tensorflow').disabled = True
os.environ['PYTHONIOENCODING'] = 'UTF-8'


# Numpy pre-processed audio files are listed here

# Numpy pre-processed audio files are listed here
array_of_feature_set_names = ["All_data_1000ms_22050hz\\0-8_(REAL)_0-56_(FAKE)_1000ms_for_sample_22050hz_frequency_DeepVoice_dataset_feature_set.npy",
                              "All_data_1000ms_22050hz\\0-31779_samples_1000ms_for_sample_22050hz_frequency_InTheWild_dataset_feature_set.npy",
                              "All_data_1000ms_22050hz\\0-30043_(REAL)_0-0_(FAKE)_1000ms_for_sample_22050hz_frequency_FluentSpeechCorpus_feature_set.npy",
                              "All_data_1000ms_22050hz\\0-3106_(REAL)_0-16283_(FAKE)_1000ms_for_sample_22050hz_frequency_WaveFake_dataset_feature_set.npy"]
                              "All_data_1000ms_22050hz\\0-3106_(REAL)_0-16283_(FAKE)_1000ms_for_sample_22050hz_frequency_WaveFake_dataset_feature_set.npy"]

array_of_labels_set_names = [ "All_data_1000ms_22050hz\\0-8_(REAL)_0-56_(FAKE)_1000ms_for_sample_22050hz_frequency_DeepVoice_dataset_labels_set.npy",
                              "All_data_1000ms_22050hz\\0-31779_samples_1000ms_for_sample_22050hz_frequency_InTheWild_dataset_labels_set.npy",
                              "All_data_1000ms_22050hz\\0-30043_(REAL)_0-0_(FAKE)_1000ms_for_sample_22050hz_frequency_FluentSpeechCorpus_labels_set.npy",
                              "All_data_1000ms_22050hz\\0-3106_(REAL)_0-16283_(FAKE)_1000ms_for_sample_22050hz_frequency_WaveFake_dataset_labels_set.npy"]
                              "All_data_1000ms_22050hz\\0-3106_(REAL)_0-16283_(FAKE)_1000ms_for_sample_22050hz_frequency_WaveFake_dataset_labels_set.npy"]

# Class names
# Class names
class_names = ["fake", "real"]

# Create a list of all the features
# Create a list of all the features
train_data = []
for dataset_features_name in array_of_feature_set_names:
    destination_dataset = 'Audio_numpy_files\\' + dataset_features_name
    print(destination_dataset)
    train_data.append((np.load(destination_dataset))[0:5000])

train_data = np.concatenate(train_data, axis=0)

# Create a list of all the labels
# Create a list of all the labels
labels = []
for dataset_labels_name in array_of_labels_set_names:
    destination_dataset = 'Audio_numpy_files\\' + dataset_labels_name
    print(destination_dataset)
    labels.append((np.load(destination_dataset))[0:5000])

labels = np.concatenate(labels, axis=0)
labels = labels.astype('int32')
    

# Scale the audio data using RobustScaler
    

# Scale the audio data using RobustScaler
scaler = RobustScaler()
train_data = scaler.fit_transform(train_data)

# Save the scaler
scaler_filename = "scaler.save"
# Save the scaler
scaler_filename = "scaler.save"
import pickle
with open(scaler_filename, 'wb') as file:
with open(scaler_filename, 'wb') as file:
    pickle.dump(scaler, file)

# Split the data into training, validation and testing sets
# Split the data into training, validation and testing sets
x_train, x_test, y_train, y_test = train_test_split(train_data, labels, test_size=0.25, random_state=123)
x_train, x_val, y_train, y_val = train_test_split(x_train, y_train, test_size=0.25, random_state=123)

# Create the model
# Create the model
inputs = layers.Input(shape=(x_train.shape[1], 1))
CNNmodel = models.Sequential([
    inputs,
    layers.Conv1D(64, kernel_size=3, activation='relu', input_shape=(x_train.shape[1], 1)),
    layers.MaxPooling1D(pool_size=2),
    layers.Dropout(0.2),
    layers.Conv1D(64, kernel_size=3, activation='relu'),
    layers.MaxPooling1D(),
    layers.Dropout(0.2),
    layers.Conv1D(64, kernel_size=3, activation='relu'),
    layers.Flatten(),
    layers.Dense(64, activation='relu'),
    layers.Dropout(0.2),
    layers.Dense(32, activation='relu'),
    layers.Dense(1, activation='sigmoid')
    
    # layers.Conv1D(128, kernel_size=3, activation='relu', input_shape=(x_train.shape[1], 1)),
    # layers.MaxPooling1D(pool_size=2),
    # layers.Dropout(0.2),
    # layers.Conv1D(128, kernel_size=3, activation='relu'),
    # layers.MaxPooling1D(),
    # layers.Dropout(0.2),
    # layers.Conv1D(128, kernel_size=3, activation='relu'),
    # layers.MaxPooling1D(),
    # layers.Dropout(0.2),
    # layers.Conv1D(128, kernel_size=3, activation='relu'),
    # layers.MaxPooling1D(),
    # layers.Dropout(0.2),
    # layers.Conv1D(128, kernel_size=3, activation='relu'),
    # layers.Flatten(),
    # layers.Dense(128, activation='relu'),
    # layers.Dropout(0.2),
    # layers.Dense(64, activation='relu'),
    # layers.Dropout(0.2),
    # layers.Dense(32, activation='relu'),
    # layers.Dense(24, activation='softmax')
])


# Display a summary of the models structure
CNNmodel.summary()

# Build the model
CNNmodel.compile(optimizer='adam', loss=keras.losses.BinaryCrossentropy(), metrics=['accuracy', 'precision', 'recall' ])

# Train the model
# Train the model
history = CNNmodel.fit(x_train,y_train, batch_size=256, epochs=3, validation_data= (x_val, y_val))

# Save the model
# Save the model
CNNmodel.save("2_Audio_model.keras")

# Evaluate the model
# Evaluate the model
predict_x=CNNmodel.predict(x_test)
predicted_classes = (predict_x >= 0.5).astype("int32")
counter = 0

threshold = 0.5

for i in range(len(predict_x)):
    if predict_x[i] >= threshold:
        counter += 1
print("Size: ", len(predict_x), "Counter: ", counter)

print(classification_report(y_test, predicted_classes, target_names=class_names))

from sklearn.metrics import confusion_matrix

# Calculate the confusion matrix
cm = confusion_matrix(y_test, predicted_classes)

# Print the confusion matrix
print("Confusion Matrix:")
print(cm)