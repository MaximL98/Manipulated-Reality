import keras

from model import model

## Get frames and their labels
# frames, label = 
## Build the model
# model.build(frames)
## Visualize the model
# keras.utils.plot_model(model, expand_nested=True, dpi=60, show_shapes=True)
## Train the model
## Binary classification problems with two classes, the most appropriate loss function is Binary Crossentropy
# model.compile(loss = keras.losses.BinaryCrossentropy(from_logits=True), 
#              optimizer = keras.optimizers.Adam(learning_rate = 0.0001), 
#             metrics = ['accuracy'])

## Better to start with less epochs 20-30
# history = model.fit(x = train_ds,
#                    epochs = 50, 
#                   validation_data = val_ds)
## need to return history
