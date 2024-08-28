import random
import pathlib
import itertools
import collections

import cv2
import numpy as np
import matplotlib.pyplot as plt
#import eniops

import tensorflow as tf
import keras
from keras import layers
#LSTM


# Layer that performs a two-step convolution, firstly extracts spatial features from the data 
# Then captures temporal dependencies within the data across multiple time steps based on the extracted spatial features.
class Conv2Plus1D(keras.layers.Layer):
  def __init__(self, filters, kernel_size, padding):
    super().__init__()
    self.seq = keras.Sequential([  
        # Spatial decomposition, focus on one frame at a time
        layers.Conv3D(filters=filters,
                      kernel_size=(1, kernel_size[1], kernel_size[2]),
                      padding=padding),
        # Temporal decomposition, focus on time dimension
        layers.Conv3D(filters=filters, 
                      kernel_size=(kernel_size[0], 1, 1),
                      padding=padding)
        ])
  # Responsible for performing the actual computation of the layer
  def call(self, x):
    # Get output from the convolutional layers
    return self.seq(x) 
  

# Residual layer of the model with convolution, layer normalization, and activation function, ReLU.
class ResidualMain(keras.layers.Layer):
  def __init__(self, filters, kernel_size):
    super().__init__()
    self.seq = keras.Sequential([
        # Captures some initial features
        Conv2Plus1D(filters=filters,
                    kernel_size=kernel_size,
                    padding='same'),
        # Normalization across all channels of the feature maps extracted by the previous convolution
        layers.LayerNormalization(),
        # Activation function to introduce non-linearity
        layers.ReLU(),
        # Further refines features
        Conv2Plus1D(filters=filters, 
                    kernel_size=kernel_size,
                    padding='same'),
        # Normalization across all channels of the feature maps extracted by the previous convolution
        layers.LayerNormalization()
    ])

  # Performing the computation of the layer 
  def call(self, x):
    return self.seq(x)


# The Project layer with a Dense layer used to reduce the dimensionality of these features,
# Potentially leading to a more efficient network and reducing the risk of overfitting.
class Project(keras.layers.Layer):
  def __init__(self, units):
    super().__init__()
    self.seq = keras.Sequential([
        # Dense (fully-connected) transformation to the input data
        layers.Dense(units),
        # Normalization across all channels of the features produced by the dense layer
        layers.LayerNormalization()
    ])

  def call(self, x):
    return self.seq(x)
  
# The ResizeVideo layer leverages the einops library for efficient video resizing within a Keras model
'''class ResizeVideo(keras.layers.Layer):
  def __init__(self, height, width):
    super().__init__()
    self.height = height
    self.width = width
    self.resizing_layer = layers.Resizing(self.height, self.width)

  def call(self, video):
    # b stands for batch size, t stands for time, h stands for height, 
    # w stands for width, and c stands for the number of channels.
    # Batch size (b), number of frames (t), height (h), width (w), and number of channels (c)
    old_shape = einops.parse_shape(video, 'b t h w c')
    images = einops.rearrange(video, 'b t h w c -> (b t) h w c')
    images = self.resizing_layer(images)
    videos = einops.rearrange(
        images, '(b t) h w c -> b t h w c',
        t = old_shape['t'])
    return videos'''