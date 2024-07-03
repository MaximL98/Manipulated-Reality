
import keras
import numpy as np

from model import get_model
from utils import batch_generator, load_data_from_csv
from data import paths_to_csv


batch_size = 8
train_generator, train_labels = batch_generator(paths_to_csv['train_df'], batch_size)
test_generator, test_labels = batch_generator(paths_to_csv['test_df'], batch_size, is_training=False)
val_generator, val_labels = batch_generator(paths_to_csv['val_df'], batch_size, is_training=False)


model = get_model()
## Build the model
model.build(input_shape=(None, 225, 224, 224, 3))
## Visualize the model
#keras.utils.plot_model(model, expand_nested=True, dpi=60, show_shapes=True)
## Train the model
## Binary classification problems with two classes, the most appropriate loss function is Binary Cross entropy
model.compile(loss = keras.losses.BinaryCrossentropy(from_logits=True), 
              optimizer = keras.optimizers.Adam(learning_rate = 0.0001),
              metrics = ['accuracy'])

print("Starting to train model...")
## Better to start with less epochs 20-30
#history = model.fit(x = train_generator,epochs = 20, validation_data = val_generator)

model.fit(x=train_generator, y=train_labels, epochs=10)
# Evaluate on test data
test_results = model.evaluate(test_generator, return_dict=True)
print("Test results:", test_results)