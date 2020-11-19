import pytesseract
import pandas as pd
import cv2
import numpy as np


def extractCoordsData(img):
    #Text recognization using tessaract and Pytessract
    hImg,wImg= img.shape
    detected_text_df = pytesseract.image_to_data(img,lang='script/Devanagari',output_type=pytesseract.Output.DATAFRAME,config='--oem 3 --psm 6')

    detected_text_df = detected_text_df[['text','left','top','width','height']]
    detected_text_df = detected_text_df.dropna()
    
    d = {}
    d['data'] = detected_text_df
    d['height'] = hImg
    d['width'] = wImg

    return d


def convertToExel(data):
    scale_factor = 120
    width = int(data['width']/scale_factor)
    height = int(data['height']/scale_factor)
    detected_text_df = data['data']

    x_cord = []
    y_cord = []
    e_text = []


    for index, row in detected_text_df.iterrows():
        x = int(row['left']/scale_factor)
        y = int(row['top']/scale_factor)
        
        x_cord.append(x)
        y_cord.append(y)
        e_text.append(row['text'])

    xc = pd.Series(x_cord,name='x_cord')
    yc = pd.Series(y_cord,name='y_cord')
    tc = pd.Series(e_text,name='e_text')


    exel_meta = pd.DataFrame('', index=range(height), columns=range(width))
    
    for i,t in enumerate(tc):
        if exel_meta[xc[i]][yc[i]]=='':
            exel_meta[xc[i]][yc[i]] = t

    return exel_meta  









