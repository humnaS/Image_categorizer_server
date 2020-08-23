from tensorflow.keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
import PIL
import cv2
import os
import numpy as np
import pickle 
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.applications import vgg16
from tensorflow.keras.models import Model
import tensorflow.keras

from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, InputLayer
from tensorflow.keras.models import Sequential
from tensorflow.keras import optimizers

import h5py


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

model.compile(loss='binary_crossentropy',
            optimizer=optimizers.RMSprop(lr=1e-5),
            metrics=['accuracy'])


datagen = ImageDataGenerator(
        rotation_range=25,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.3,
        horizontal_flip=True,
        fill_mode='nearest')

def Data_Augmentation(DATA_DIR,CATEGORIES_FOLDER):

    for category in CATEGORIES_FOLDER:
        path=os.path.join(DATA_DIR,category) 
        img_path=path.split('/')
        img_folder=img_path[-1]
    
        for img in os.listdir(path):
            print("path: ",path)
            print(path+"/"+img)
            
            inner_path=path+"/"+img
            img = load_img(inner_path)  # this is a PIL image
            x = img_to_array(img)  # this is a Numpy array with shape (300, 300, 3)
            x = x.reshape((1,) + x.shape)  # this is a Numpy array with shape (1, 300, 300, 3)
            x.shape
            # # the .flow() command below generates batches of randomly transformed images
            # # and saves the results to the `preview/` directory
            i = 0
            
            for batch in datagen.flow(x, batch_size=1,
                                    save_to_dir=path,save_format='jpeg'):
                i += 1
                if i > 1:
                    break
            
        
def create_training_data(DATA_DIR,CATEGORIES,IMG_SIZE):
    training_data=[]

    for category in CATEGORIES:
        path=os.path.join(DATA_DIR,category) 
        class_num=CATEGORIES.index(category)
       
        for img in os.listdir(path):
            try:
                img_arr=cv2.imread(os.path.join(path,img))
                img_arr=cv2.cvtColor(img_arr,cv2.COLOR_BGR2RGB)
                new_array=cv2.resize(img_arr,(IMG_SIZE,IMG_SIZE))
                training_data.append([new_array,class_num])
            except Exception as e:
              
                print(e)
                pass

    return training_data

def Data_Pre_Processing(DATA_DIR,CATEGORIES):

    X=[]
    y=[]
    
    IMG_SIZE=200
        
    training_data = create_training_data(DATA_DIR,CATEGORIES,IMG_SIZE)
    
    for features,label in training_data:
        X.append(features)
        y.append(label)


    X=np.array(X).reshape(-1,IMG_SIZE,IMG_SIZE,3)

  
    return X,y

def Model(X,y):
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


    model = Sequential()
    model.add(vgg_model)
    model.add(Dense(512, activation='relu', input_dim=input_shape))
    model.add(Dropout(0.3))
    model.add(Dense(512, activation='relu'))
    model.add(Dropout(0.3))
    model.add(Dense(1, activation='sigmoid'))

    model.compile(loss='binary_crossentropy',
                optimizer=optimizers.RMSprop(lr=1e-5),
                metrics=['accuracy'])
   
    print(model.summary())

    return model


def Model_Train(DIR_NAME,categories):
   
    Data_Augmentation(DIR_NAME,categories)

    X,y = Data_Pre_Processing(DIR_NAME,categories)
    
    print("Completed Pre-Processing")
    print(len(X),len(y))

    print(model.summary())
    history = model.fit(X,np.array(y),epochs=5,validation_split=0.2)
    print(history)
    model_name = "model.h5"
    model_path = DIR_NAME + "/" + model_name
    model.save(model_path, include_optimizer=False)

    temp = history.history

    retJson = {"status":200,"msg":"Model trained successfully","history": str(temp)}
    tf.keras.backend.clear_session()
    return retJson

def Delete_Data(proj_path,categories):
    DATA_DIR = proj_path
    CATEGORIES_FOLDER = categories

    for category in CATEGORIES_FOLDER:
        path=os.path.join(DATA_DIR,category) 
        img_path=path.split('/')
        img_folder=img_path[-1]
    
        for img in os.listdir(path):
            image_path =  path+"/"+img
            os.remove(image_path)
            print(image_path+" deleted!")