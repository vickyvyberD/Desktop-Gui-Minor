import os
#import logging
import numpy as np
from keras.models import model_from_json
import cv2 #image processing
#from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import Flatten
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D
from keras.utils import np_utils
from keras import backend as K

K.set_image_data_format('channels_last') #NHWC 

loaded_model = None

with open('model_final5L.json','r') as json_file :
    loaded_model = model_from_json(json_file.read())
    loaded_model.load_weights("model_final5L.h5")

def run(x) :
    #cv2 imread
    img = cv2.imread(x, cv2.IMREAD_GRAYSCALE)
    
    #image convert
    #img = x.convert('L')
    #img = np.array(img)
    
    if img is not None:
        # images.append(img)
        img = ~img
        retval, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)               #THRESHholding
        ctrs, retval = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) #CONTOUR DETECTION which returns  4 points and contours
        cnt = sorted(ctrs, key=lambda ctr: cv2.boundingRect(ctr)[0])                #bounding rectangles sorted according to their x distances
        w = int(28)
        h = int(28)
        train_data = []
        # print(len(cnt))
        rects = []
        for c in cnt:                                                               #saving each rectangle found
            x, y, w, h = cv2.boundingRect(c)
            rect = [x, y, w, h]
            rects.append(rect)
        # print(rects)
        bool_rect = []                                                              #checking if each digit is properly distanced
        for r in rects:
            l = []
            for rec in rects:
                flag = 0
                if rec != r:
                    if r[0] < (rec[0]+rec[2]+8) and rec[0] < (r[0]+r[2]+8) and r[1] < (rec[1]+rec[3]+8) and rec[1] < (r[1]+r[3]+8):
                        flag = 1
                    l.append(flag)
                if rec == r:
                    l.append(0)
            bool_rect.append(l)
        # print(bool_rect)
        dump_rect = []                                                              #dumping the rectangle if two rectangles are made for same digit or if digits or not well placed
        for i in range(0, len(cnt)):
            for j in range(0, len(cnt)):
                if bool_rect[i][j] == 1:
                    area1 = rects[i][2]*rects[i][3]
                    area2 = rects[j][2]*rects[j][3]
                    if(area1 == min(area1, area2)):
                        dump_rect.append(rects[i])
        # print(len(dump_rect))
        final_rect = [i for i in rects if i not in dump_rect]                        #final rectangle
        # print(final_rect)
        for r in final_rect:
            x = r[0]
            y = r[1]
            w = r[2]
            h = r[3]
            im_crop = thresh[y:y+h+10, x:x+w+10]

            im_resize = cv2.resize(im_crop, (28, 28))
            cv2.imshow("work", im_resize)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

            im_resize = np.reshape(im_resize, ( 28, 28,1))
            train_data.append(im_resize)


    s = ''
    for i in range(len(train_data)):
        train_data[i] = np.array(train_data[i])                                 #appending image data into train 
        train_data[i] = train_data[i].reshape(1,28, 28,1)                       # reshaping to NHWC
        result = loaded_model.predict_classes(train_data[i])                    # Predicting classes
        if(result[0] == 10):
            s = s+'-'
        if(result[0] == 11):
            s = s+'+'
        if(result[0] == 12):
            s = s+'*'
        if(result[0] == 0):
            s = s+'0'
        if(result[0] == 1):
            s = s+'1'
        if(result[0] == 2):
            s = s+'2'
        if(result[0] == 3):
            s = s+'3'
        if(result[0] == 4):
            s = s+'4'
        if(result[0] == 5):
            s = s+'5'
        if(result[0] == 6):
            s = s+'6'
        if(result[0] == 7):
            s = s+'7'
        if(result[0] == 8):
            s = s+'8'
        if(result[0] == 9):
            s = s+'9'
        if(result[0] == 13):
            s = s+'/'
        if(result[0] == 14):
            s = s+'('
        if(result[0] == 15):
            s = s+')'
    return s

