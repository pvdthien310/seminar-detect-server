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
tsr.pytesseract.tesseract_cmd ='C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

def Detect(base64_string):
    # original_file_path = 'TEST5.png'
    # img = cv.imread(original_file_path, cv.IMREAD_UNCHANGED)
    # img = cv.cvtColor(img, cv.COLOR_BGR2RGB)  
    original_file_path = "Result"
    im_bytes = base64.b64decode(base64_string)
    im_arr = np.frombuffer(im_bytes, dtype=np.uint8)  # im_arr is one-dim Numpy array
    img = cv.imdecode(im_arr, flags=cv.IMREAD_COLOR)
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    boxes = tsr.image_to_data(img)
    i = 0
    j = 0
    array = []

    rectangle = []
    paragagphInfo= []

    for x,b in enumerate(boxes.splitlines()):
        if x!=0:
            b = b.split()
            if len(b) == 12:
                print(b)
                array.append(b)
                if [int(b[2]),int(b[4])] not in paragagphInfo: paragagphInfo.append([int(b[2]),int(b[4])])


    for index in paragagphInfo:
        sub_rectangle = []
        for value in array:
            if int(value[2]) == index[0] and int(value[4]) == index[1]: 
                sub_rectangle.append([int(value[6]), int(value[7]), int(value[8]), int(value[9]), value[2], value[4]])
        rectangle.append(sub_rectangle)

    split_index = [] # x1,y1,xmax,wmax,hmax, ymin, paragraph_index, line_index

    for sub_rectangle in rectangle:
        x1 = sub_rectangle[0][0]
        y1 = sub_rectangle[0][1]
        xmax = sub_rectangle[len(sub_rectangle) - 1][0]
        ymax = sub_rectangle[len(sub_rectangle) - 1][1]
        wmax = sub_rectangle[len(sub_rectangle) - 1][2]
        hmax = sub_rectangle[0][3]
        ymin = sub_rectangle[0][1]
        for vector in sub_rectangle:
            if vector[3] > hmax: hmax = vector[3]
            if vector[1] < ymin: ymin = vector[1]
        split_index.append([x1,y1,xmax,wmax,hmax,ymin,sub_rectangle[0][4],sub_rectangle[0][5]])

    # os.rmdir(original_file_path.split('.')[0])
    if (os.path.exists(original_file_path) == TRUE):
         shutil.rmtree(original_file_path)
    os.mkdir(original_file_path)

    small_img = []
    # cv.imwrite('./ori.png', img)

    for i in split_index:
        print(i)
        crop_img = img[i[5] - 5 : i[5] + i[4] + 5, i[0] - 5: i[2] + i[3] + 5 ]
        small_img.append(crop_img)
        cropped_file_path = './{original_img_path}/crop_{index}.png'.format(original_img_path = original_file_path, index = str(i[6])+'_' + str(i[7]))
        print(cropped_file_path)
        cv.imwrite(cropped_file_path, crop_img)
 
    result = []
    rs_str = ''

    config = Cfg.load_config_from_file('config_4.yml')
    config['weights'] = 'transformerocr_4.pth'
    config['cnn']['pretrained']=False
    config['device'] = 'cpu'
    config['predictor']['beamsearch']=False
    detector = Predictor(config)

    for path in os.listdir(original_file_path):
        img = original_file_path.split('.')[0] + '/' + path
        print('-------------------' + img)
        img = Image.open(img)
        # result.append(detector.predict(img))
        rs_str = rs_str + detector.predict(img) + '\n'
        print('-------------------' + 'Done')

    # for child_img in small_img:
    #     print('-------------------')
    #     rs_str = rs_str + detector.predict(child_img) + '\n'
    #     child_img = cv.cvtColor(child_img, cv.COLOR_BGR2RGB)
    #     rs_str = rs_str + detector.predict(child_img) + '\n'
    #     print('-------------------' + 'Done')

    f= open("rs.txt","w", encoding="utf-8")
    f.write(rs_str)
    f.close()
    return jsonify({"result" : rs_str})




