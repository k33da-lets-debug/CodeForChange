import numpy as np
import math
import cv2

def compute_skew(img):
    
    #load in grayscale:
    src = img
    height, width = src.shape[0:2]
    
    # #invert the colors of our image:
    cv2.bitwise_not(src, src)
    
    #Hough transform:
    minLineLength = width/2.0
    maxLineGap = 20
    lines = cv2.HoughLinesP(src,1,np.pi/180,100,minLineLength,maxLineGap)
    
    #calculate the angle between each line and the horizontal line:
    angle = 0.0
    nb_lines = len(lines)
    
    
    for line in lines:
        angle += math.atan2(line[0][3]*1.0 - line[0][1]*1.0,line[0][2]*1.0 - line[0][0]*1.0)
    
    angle /= nb_lines*1.0
    
    return angle* 180.0 / np.pi


def deskew(img,angle):
    
    # load in grayscale:
    # img = cv2.imread(file_name,0)
    
    #invert the colors of our image:
    cv2.bitwise_not(img, img)
    
    #compute the minimum bounding box:
    non_zero_pixels = cv2.findNonZero(img)
    center, wh, theta = cv2.minAreaRect(non_zero_pixels)
    
    root_mat = cv2.getRotationMatrix2D(center, angle, 1)
    rows, cols = img.shape
    rotated = cv2.warpAffine(img, root_mat, (cols, rows), flags=cv2.INTER_CUBIC)

    #Border removing:
    sizex = np.int0(wh[0])
    sizey = np.int0(wh[1])
    if theta > -45 :
        temp = sizex
        sizex= sizey
        sizey= temp
    return cv2.getRectSubPix(rotated, (sizey,sizex), center)



def skeletonize(img):
    size = np.size(img)
    skel = np.zeros(img.shape,np.uint8)
    
    ret,img = cv2.threshold(img,127,255,0)
    element = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
    done = False
    
    while( not done):
        eroded = cv2.erode(img,element)
        temp = cv2.dilate(eroded,element)
        temp = cv2.subtract(img,temp)
        skel = cv2.bitwise_or(skel,temp)
        img = eroded.copy()
    
        zeros = size - cv2.countNonZero(img)
        if zeros==size:
            done = True
    
    return skel


def remove_noise(img):
    #dialate
    kernel = np.ones((5, 5), np.uint8)
    cv2.dilate(img, kernel, iterations = 1)

    #erode
    kernel = np.ones((5, 5), np.uint8)
    cv2.erode(img, kernel, iterations = 1)

    cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
    res=cv2.medianBlur(img, 3)

    return res



