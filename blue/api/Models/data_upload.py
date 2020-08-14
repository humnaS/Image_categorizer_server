from flask import Blueprint,jsonify, request
from flask_restful import Api,Resource
import pandas as pd
import os
from PIL import Image
from io import BytesIO
import requests
from PIL import Image
import urllib
import numpy as np


def Upload_Data(cat_path,url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    
    imgarr = np.array(img) 

    #print(imgarr)
    #filename = url.split('.')[-2]
    filename = url.split('/')[-1]
    name = filename.split('.')[-2]
    #print(name)
    ext = filename.split('.')[-1]
    #print(ext)
    fn = name + '.' + ext 
    image = Image.fromarray(imgarr, 'RGB')
    location = os.path.join(cat_path, fn)
    image.save(location)
   

    return "Uploaded Successfully"