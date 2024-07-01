
import keras
import numpy as npc

from model import model
from utils import batch_generator, load_data_from_csv
from data import paths_to_csv


'''batch_size = 4
train_generator = batch_generator(paths_to_csv['train_df'], batch_size)
test_generator = batch_generator(paths_to_csv['test_df'], batch_size, is_training=False)
val_generator = batch_generator(paths_to_csv['val_df'], batch_size, is_training=False)'''


train_data, train_labels = load_data_from_csv(paths_to_csv['train_df'])
test_data, test_labels = load_data_from_csv(paths_to_csv['test_df'])
val_data, val_labels = load_data_from_csv(paths_to_csv['val_df'])

model_ = model()

#for batch_videos, batch_labels,  in train_generator:
## Get frames and their labels
#frames, label = next(iter(train_generator))
    ## Build the model
model_.build(input_shape=(None, 225, 224, 224, 3))
## Visualize the model
keras.utils.plot_model(model_, expand_nested=True, dpi=60, show_shapes=True)
## Train the model
## Binary classification problems with two classes, the most appropriate loss function is Binary Cross entropy
model_.compile(loss = keras.losses.BinaryCrossentropy(from_logits=True), 
              optimizer = keras.optimizers.Adam(learning_rate = 0.0001), 
              metrics = ['accuracy'])

## Better to start with less epochs 20-30
history = model_.fit(x = train_data,
                    epochs = 50, 
                    validation_data = val_data)
## need to return history
model_.evaluate(test_data, return_dict=True)