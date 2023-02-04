from tkinter import TRUE
import cv2 as cv
import pytesseract as tsr
import os
import numpy as np
import shutil
import base64
from vietocr.tool.predictor import Predictor
from vietocr.tool.config import Cfg
import matplotlib.pyplot as plt
from PIL import Image
from flask import jsonify

def Detect(base64_string):
    im_bytes = base64.b64decode(base64_string)
    f = open("aaaa.txt", "a")
    f.write(base64_string)
    f.close()

    im_arr = np.frombuffer(im_bytes,np.uint8)  # im_arr is one-dim Numpy array
    img = cv.imdecode(im_arr, flags=cv.IMREAD_COLOR)
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
   
    resized_image = cv.threshold(img, 250 ,255, cv.THRESH_BINARY)
    # resized_image = cv.resize(resized_image, (1200, 900)) 
    img2 = np.array(img)
    
    cv.imshow('sample image',resized_image)
    cv.waitKey(0) # waits until a key is pressed
    cv.imshow('sample image original',img)
    cv.waitKey(0)
    cv.destroyAllWindows()
    return 0
