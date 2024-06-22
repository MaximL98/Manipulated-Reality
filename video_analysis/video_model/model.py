import keras
from keras import layers

from model_layers import Conv2Plus1D
from utils import add_residual_block

# Manipulated reality video model architecture 
def model(HEIGHT, WIDTH):
    # Train and evaluate the model using different frame selections (e.g., 10, 50, 100, 200), processed data now is 200 frames.
    input_shape = (None, 200, HEIGHT, WIDTH, 3)
    # Handle videos with different batch sizes.
    input = layers.Input(shape=(input_shape[1:]))
    x = input

    # Experiment with smaller spatial kernel sizes(e.g., 3x3 or 5x5), and not 7x7
    x = Conv2Plus1D(filters=16, kernel_size=(3, 7, 7), padding='same')(x)
    x = layers.BatchNormalization()(x)
    x = layers.ReLU()(x)

    # Resizing is good practice, as it helps with computational efficiency and focus on relevant information
    # Only problem is ofc loss of information
    # BUT might not be needed because, training data consist of faces only!!!
    #x = ResizeVideo(HEIGHT // 2, WIDTH // 2)(x)

    # Block 1
    x = add_residual_block(x, 16, (3, 3, 3))
    #x = ResizeVideo(HEIGHT // 4, WIDTH // 4)(x)

    # Block 2
    x = add_residual_block(x, 32, (3, 3, 3))
    #x = ResizeVideo(HEIGHT // 8, WIDTH // 8)(x)

    # Block 3
    x = add_residual_block(x, 64, (3, 3, 3))
    #x = ResizeVideo(HEIGHT // 16, WIDTH // 16)(x)

    # Block 4
    x = add_residual_block(x, 128, (3, 3, 3))

    # Reduces the feature maps to a single vector representing the average activations for each feature
    x = layers.GlobalAveragePooling3D()(x)
    # Flattens the pooled output into a 1D vector
    x = layers.Flatten()(x)
    # Performs linear classification, mapping the flattened features to 2 class probabilities
    x = layers.Dense(2)(x)

    model = keras.Model(input, x)
    return model


