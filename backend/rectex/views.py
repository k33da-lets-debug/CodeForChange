from django.shortcuts import render
from django.http import HttpResponse
from PIL import Image
import pytesseract
import cv2
import numpy as np
from .image_transformation_utils import compute_skew,deskew,skeletonize,remove_noise
# Create your views here.

def rectex_view(request):

    #TODO:
    # 1. Get image
    raw_image = cv2.imread('staticroot/test_ocr_images/Sample712.png')

    # 2. Convert it to rgb
    rgb_image = cv2.cvtColor(raw_image,cv2.COLOR_BGR2RGB)

    # 2.1 binarization: converting to black and white pixels
    grayscale_image = cv2.cvtColor(rgb_image,cv2.COLOR_RGB2GRAY)    

    #Remove noise
    adaptive_threshold = cv2.adaptiveThreshold(grayscale_image,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,81,10)
    #Sharpen text
    adaptive_threshold = cv2.adaptiveThreshold(adaptive_threshold, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 5, 4)

    cv2.imwrite('staticroot/test_ocr_images/threshresult.png',adaptive_threshold)

    # 2.2 Noise removal: Removing patches, dots etc
    # noise_removed = remove_noise(adaptive_threshold)
    # cv2.imwrite('staticroot/test_ocr_images/noiseremovalresult.png',noise_removed)

    # 2.3 Skew correction: Setting orientation (Hough transformation)
    # computed_skew = compute_skew(adaptive_threshold)
    # deskewed = deskew(adaptive_threshold,computed_skew)
    # cv2.imwrite('staticroot/test_ocr_images/dskewedresult.png',deskewed)


    # 2.4 Thinning and Skeletonization: 
    # skeletonized = skeletonize(background_noise_reduced)
    # cv2.imwrite('staticroot/test_ocr_images/skeletonizationresult.png',skeletonized)

    # 3. Apply some filters


    # 4. Recognize text

    # 5. Add bounded boxes, confidance code to recgonized text

    # 6. Display text and image with recognized text

    # 7. Do some NLP magic

    return HttpResponse('<h1>'+str(pytesseract.image_to_string(adaptive_threshold,lang='script/Devanagari'))+'</h1>')
