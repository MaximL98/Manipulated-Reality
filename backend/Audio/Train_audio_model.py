import os
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

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

train_data = np.load('feature_set.npy')

labels = np.load('labels.npy')
labels = labels.astype('int32')

print(train_data.dtype)
print(labels.dtype)
print(train_data[0][0].dtype)

scaler = MinMaxScaler((-1, 1))
train_data = scaler.fit_transform(train_data)


x_train, x_test, y_train, y_test = train_test_split(train_data, labels, test_size=0.25, random_state=123)
x_train, x_val, y_train, y_val = train_test_split(x_train, y_train, test_size=0.25, random_state=123)

print(x_train.shape)

print(len(labels))

print("x_train shape:", x_train.shape)
print("x_val shape:", x_val.shape)

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
    layers.Dense(24, activation='softmax')
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

# Build the model
CNNmodel.compile(optimizer='adam', loss=tf.keras.losses.sparse_categorical_crossentropy, metrics=['accuracy'])

# Display a summary of the models structure
CNNmodel.summary()

history = CNNmodel.fit(x_train,y_train, batch_size=128, epochs=20, validation_data= (x_val, y_val))
