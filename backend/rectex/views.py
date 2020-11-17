from django.shortcuts import render
from django.http import HttpResponse
from PIL import Image
import pytesseract
import cv2
import numpy as np
from .image_transformation_utils import compute_skew,deskew,skeletonize,remove_noise,remove_lines
# Create your views here.

# def rectex_view(request):

#     #TODO:
#     # 1. Get image
#     raw_image = cv2.imread('staticroot/test_ocr_images/Test.jpg')
#     # 2. Convert it to rgb
#     rgb_image = cv2.cvtColor(raw_image,cv2.COLOR_BGR2RGB)
#     # Convert it to greyscale
#     grayscale_image = cv2.cvtColor(rgb_image,cv2.COLOR_RGB2GRAY)  
#     # 2.1 binarization: converting to black and white pixels, and removing watermark
#     # define a threshold, 128 is the middle of black and white in grey scale
#     # threshold the image
#     thresh = 128
#     img_binary = cv2.threshold(grayscale_image, thresh, 255, cv2.THRESH_BINARY)[1] 

#     #Text thickning
#     kernel = np.ones((1,1), np.uint8) 
#     text_thickning = cv2.erode(img_binary,kernel,iterations = 2)
#     cv2.imwrite('staticroot/test_ocr_images/threshresult.png',text_thickning)

#     #Removing H/V lines
#     removed_lines = remove_lines(text_thickning)
#     cv2.imwrite('staticroot/test_ocr_images/removed_lines.png',removed_lines)

#     # Skew correction: Setting orientation (Hough transformation)
#     # computed_skew = compute_skew(adaptive_threshold)
#     # deskewed = deskew(adaptive_threshold,computed_skew)
#     # cv2.imwrite('staticroot/test_ocr_images/dskewedresult.png',deskewed)

#     # Thinning and Skeletonization: 
#     # skeletonized = skeletonize(background_noise_reduced)
#     # cv2.imwrite('staticroot/test_ocr_images/skeletonizationresult.png',skeletonized)

#     # Text recognization using tessaract and Pytessract
#     # hImg,wImg= removed_lines.shape
#     # detected_text = pytesseract.image_to_data(removed_lines,lang='script/Devanagari')
#     # #print(detected_text)
#     # bound_result = None
#     # for x,b in enumerate(detected_text.splitlines()):
#     #     if x!=0:
#     #         b = b.split() 
#     #         if len(b)==12:
#     #             a,b,w,h = int(b[6]),int(b[7]) ,int(b[8]) ,int(b[9]) 
#     #             bound_result = cv2.rectangle(removed_lines,(a,b),(w+a,h+b),(0,0,255),3)
#     #             # cv2.puttext(img_erosion,b[0],(a,hImg-b+25),cv2.FONT_HERSHEY_COMPLEX,1,(50,50,255),2)

#     # # 5. Add bounded boxes, confidance code to recgonized text
#     # cv2.imwrite('staticroot/test_ocr_images/boundresult.png',bound_result)

    

#     # 6. Display text and image with recognized text

#     # 7. Do some NLP magic


#     return HttpResponse('<h1>'+str(pytesseract.image_to_string(removed_lines,lang='script/Devanagari'))+'</h1>')


# Dummy code
def rectex_view(request):
    context={}
    return render(request,'rectex/rectex_template.html',context=context)