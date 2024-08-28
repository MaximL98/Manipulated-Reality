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

class_names = ["fake", "real"]

# #train_data = np.load('feature_set.npy')
# train_data = np.load("Audio_numpy_files\\0(REAL)_to_1(REAL)_0(FAKE)_to_1(FAKE)_samples_DeepVoice_dataset_feature_set.npy")

# # labels = np.load('labels.npy')
# labels = np.load("Audio_numpy_files\\0(REAL)_to_1(REAL)_0(FAKE)_to_1(FAKE)_samples_DeepVoice_dataset_labels_set.npy")
# labels = labels.astype('int32')

array_of_feature_set_names = ["All_data_1000ms_22050hz\\0-8_(REAL)_0-56_(FAKE)_1000ms_for_sample_22050hz_frequency_DeepVoice_dataset_feature_set.npy",
                              "All_data_1000ms_22050hz\\0-31779_samples_1000ms_for_sample_22050hz_frequency_InTheWild_dataset_feature_set.npy",
                              "All_data_1000ms_22050hz\\0-30043_(REAL)_0-0_(FAKE)_1000ms_for_sample_22050hz_frequency_FluentSpeechCorpus_feature_set.npy",
                              "All_data_1000ms_22050hz\\0-3106_(REAL)_0-16283_(FAKE)_1000ms_for_sample_22050hz_frequency_WaveFake_dataset_feature_set.npy"
]

array_of_labels_set_names = [ "All_data_1000ms_22050hz\\0-8_(REAL)_0-56_(FAKE)_1000ms_for_sample_22050hz_frequency_DeepVoice_dataset_labels_set.npy",
                              "All_data_1000ms_22050hz\\0-31779_samples_1000ms_for_sample_22050hz_frequency_InTheWild_dataset_labels_set.npy",
                              "All_data_1000ms_22050hz\\0-30043_(REAL)_0-0_(FAKE)_1000ms_for_sample_22050hz_frequency_FluentSpeechCorpus_labels_set.npy",
                              "All_data_1000ms_22050hz\\0-3106_(REAL)_0-16283_(FAKE)_1000ms_for_sample_22050hz_frequency_WaveFake_dataset_labels_set.npy"
                              
]

# array_of_feature_set_names = [ "5_10_percent_1000ms_22050hz\\0-4_(REAL)_0-4_(FAKE)_1000ms_for_sample_DeepVoice_dataset_feature_set.npy",
#                               "5_10_percent_1000ms_22050hz\\0-1500_(REAL)_0-1500_(FAKE)_1000ms_for_sample_WaveFake_dataset_feature_set.npy",
#                               "5_10_percent_1000ms_22050hz\\0-1500_(REAL)_0-0_(FAKE)_1000ms_for_sample_FluentSpeechCorpus_dataset_feature_set.npy",
#                               "5_10_percent_1000ms_22050hz\\0-1500_samples_1000ms_for_sample_InTheWild_dataset_feature_set.npy"
# ]

# array_of_labels_set_names = ["5_10_percent_1000ms_22050hz\\0-4_(REAL)_0-4_(FAKE)_1000ms_for_sample_DeepVoice_dataset_labels_set.npy",
#                               "5_10_percent_1000ms_22050hz\\0-1500_(REAL)_0-1500_(FAKE)_1000ms_for_sample_WaveFake_dataset_labels_set.npy",
#                               "5_10_percent_1000ms_22050hz\\0-1500_(REAL)_0-0_(FAKE)_1000ms_for_sample_FluentSpeechCorpus_dataset_labels_set.npy",
#                               "5_10_percent_1000ms_22050hz\\0-1500_samples_1000ms_for_sample_InTheWild_dataset_labels_set.npy"
# ]

# array_of_feature_set_names = [ "2_5_percent_1000ms\\0-1_(REAL)_0-1_(FAKE)_samples_DeepVoice_dataset_feature_set.npy",
#                               "2_5_percent_1000ms\\0-1000_(REAL)_0-0_(FAKE)_samples_FluentSpeechCorpus_dataset_feature_set.npy",
#                               "2_5_percent_1000ms\\0-500_(REAL)_0-367_(FAKE)_samples_InTheWild_dataset_feature_set.npy"
# ]

# array_of_labels_set_names = ["2_5_percent_1000ms\\0-1_(REAL)_0-1_(FAKE)_samples_DeepVoice_dataset_labels_set.npy",
#                               "2_5_percent_1000ms\\0-1000_(REAL)_0-0_(FAKE)_samples_FluentSpeechCorpus_dataset_labels_set.npy",
#                               "2_5_percent_1000ms\\0-500_(REAL)_0-367_(FAKE)_samples_InTheWild_dataset_labels_set.npy"
# ]





class_names = ["fake", "real"]

train_data = []
for dataset_features_name in array_of_feature_set_names:
    destination_dataset = 'Audio_numpy_files\\' + dataset_features_name
    print(destination_dataset)
    train_data.append((np.load(destination_dataset))[0:5000])

train_data = np.concatenate(train_data, axis=0)

labels = []
for dataset_labels_name in array_of_labels_set_names:
    destination_dataset = 'Audio_numpy_files\\' + dataset_labels_name
    print(destination_dataset)
    labels.append((np.load(destination_dataset))[0:5000])

labels = np.concatenate(labels, axis=0)
labels = labels.astype('int32')

print("***************Before scaling****************")
for i in range(20):
    print(train_data[-i-10], " label: " , labels[-i-10])
    

#scaler = MinMaxScaler((-1, 1))
scaler = RobustScaler()
train_data = scaler.fit_transform(train_data)

import pickle

with open('scaler.pkl', 'wb') as file:
    pickle.dump(scaler, file)



print("***************After scaling****************")
for i in range(20):
    print(train_data[-i-10], " label: " , labels[-i-10])

####################################################### TEST ####################################################################
test_dataset_one_file = np.load("Audio_numpy_files\\All_data_1000ms_22050hz\\0-1_(REAL)_0-1_(FAKE)_1000ms_for_sample_real_fake_one_feature_set.npy")
test_dataset_one_file_labels = np.load("Audio_numpy_files\\All_data_1000ms_22050hz\\0-1_(REAL)_0-1_(FAKE)_1000ms_for_sample_real_fake_one_labels_set.npy")
test_dataset_one_file_labels = test_dataset_one_file_labels.astype('int32')
test_dataset_one_file = scaler.fit_transform(test_dataset_one_file)
####################################################### TEST ####################################################################


print(labels.shape)
print(train_data.dtype)
print(labels.dtype)
print(train_data[0][0].dtype)



x_train, x_test, y_train, y_test = train_test_split(train_data, labels, test_size=0.25, random_state=123)
x_train, x_val, y_train, y_val = train_test_split(x_train, y_train, test_size=0.25, random_state=123)

print(x_train.shape)

print(len(labels))

print("x_train shape:", x_train.shape)
print("x_train.shape[0]: ",x_train.shape[0])
print("x_train.shape[1]: ",x_train.shape[1])

print("x_val shape:", x_val.shape)


# Input shape is a tuple of 600 float32 and 1 dimension
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
# CNNmodel.add()
# CNNmodel.add(MaxPooling1D(pool_size=2))
# CNNmodel.add(Dropout(0.2))
# CNNmodel.add(Conv1D(64, kernel_size=3, activation='relu'))
# CNNmodel.add(MaxPooling1D())
# CNNmodel.add(Dropout(0.2))
# CNNmodel.add(Conv1D(64, kernel_size=3, activation='relu'))
# CNNmodel.add(Flatten())
# CNNmodel.add(Dense(64, activation='relu'))
# CNNmodel.add(Dropout(0.2))
# CNNmodel.add(Dense(32, activation='relu'))
# CNNmodel.add(Dense(24, activation='softmax'))

# Display a summary of the models structure
CNNmodel.summary()

# Build the model
CNNmodel.compile(optimizer='adam', loss=keras.losses.BinaryCrossentropy(), metrics=['accuracy', 'precision', 'recall' ])


history = CNNmodel.fit(x_train,y_train, batch_size=256, epochs=3, validation_data= (x_val, y_val))

CNNmodel.save("2_Audio_model.keras")


print(x_train.shape)
print(x_train[0].shape)
print(x_train[1].shape)
print(x_train[0][0].shape)


print(y_train)


predict_x=CNNmodel.predict(x_test)
print(predict_x[0:20])

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