from keras import layers

from model_layers import ResidualMain, Project

# Checks if the number of feature maps in the input and the block's output differ
def add_residual_block(input, filters, kernel_size):

  out = ResidualMain(filters, 
                     kernel_size)(input)

  res = input
  # Using the Keras functional APIs, project the last dimension of the tensor to
  # match the new filter size
  if out.shape[-1] != input.shape[-1]:
    res = Project(out.shape[-1])(res)

  return layers.add([res, out])
