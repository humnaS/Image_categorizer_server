from tensorflow.keras.models import load_model
import tensorflow as tf
import requests
from PIL import Image
import urllib
import numpy as np
import cv2
from io import BytesIO

def Prediction_Func(url,categories,model):
    cat_dict = {0:categories[0],1:categories[1]}
        
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    
    imgarr = np.array(img)

    # image = Image.fromarray(imgarr, 'RGB')
    print("Image: ",imgarr)

    IMG_SIZE=200
    new_array=cv2.resize(imgarr,(IMG_SIZE,IMG_SIZE))
    
    image = np.expand_dims(new_array, axis=0)
    prediction = model.predict_on_batch([image])
    pred = prediction[0][0]

    if pred < 0.30:
        result = 0
    else:
        result = 1

    prediction_result = cat_dict[result]
    retJson = {"status":200,"Predicted Category":str(prediction_result)}
    tf.keras.backend.clear_session()
    
    return retJson