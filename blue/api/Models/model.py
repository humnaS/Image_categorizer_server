from tensorflow.keras.applications import vgg16
from tensorflow.keras.models import Model
import tensorflow.keras

from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, InputLayer
from tensorflow.keras.models import Sequential
from tensorflow.keras import optimizers


input_shape = (200, 200, 3)
vgg = vgg16.VGG16(include_top=False, weights='imagenet', 
                                    input_shape=input_shape)

output = vgg.layers[-1].output
output =tensorflow.keras.layers.Flatten()(output)
vgg_model = Model(vgg.input, output)   

vgg_model.trainable = True

set_trainable = False
for layer in vgg_model.layers:
    if layer.name in ['block5_conv1', 'block4_conv1']:
        set_trainable = True
    if set_trainable:
        layer.trainable = True
    else:
        layer.trainable = False

print("Model architecture")
model = Sequential()
model.add(vgg_model)
model.add(Dense(512, activation='relu', input_dim=input_shape))
model.add(Dropout(0.3))
model.add(Dense(512, activation='relu'))
model.add(Dropout(0.3))
model.add(Dense(1, activation='sigmoid'))

print(model.summary())