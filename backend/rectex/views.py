from django.shortcuts import render,redirect
from django.http import HttpResponse
from PIL import Image
import pytesseract
import cv2
import numpy as np
from .image_transformation_utils import compute_skew,deskew,skeletonize,remove_noise,remove_lines,remove_horizontal_lines,remove_verticle_lines,get_bounded_rectangles_on_identified_text,denoise

from .forms import OCRForm
from .models import OCR

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

    context = {}
    form = OCRForm() 

    form = OCRForm()
    if request.method == 'POST':
        form = OCRForm(request.POST,request.FILES)
        if form.is_valid():
            d=form.save()
            #TODO: Optimise this pipeline
            data = OCR.objects.get(id=d.id)
            url = data.to_be_converted_image.url[1:]

            raw_image = Image.open(url)
            opencv_image = cv2.cvtColor(np.array(raw_image), cv2.COLOR_RGB2BGR)
            
            #conversion 1
            rgb_image = cv2.cvtColor(opencv_image,cv2.COLOR_BGR2RGB)
            cv2.imwrite('media/converted/cv1.png',rgb_image)
            
            #Conversion 2
            grayscale_image = cv2.cvtColor(rgb_image,cv2.COLOR_RGB2GRAY)
            cv2.imwrite('media/converted/cv2.png',grayscale_image)
            
            #Conversion 3
            binary_image = cv2.threshold(grayscale_image, 128, 255, cv2.THRESH_BINARY)[1] 
            cv2.imwrite('media/converted/cv3.png',binary_image)

            #Conversion 4
            kernel = np.ones((1,1), np.uint8) 
            text_thickned_image = cv2.erode(binary_image,kernel,iterations = 2)
            cv2.imwrite('media/converted/cv4.png',text_thickned_image)

            #Conversion 5
            removed_horizontal_lines_image = remove_horizontal_lines(text_thickned_image)
            cv2.imwrite('media/converted/cv5.png',removed_horizontal_lines_image)

            #Conversion 6
            removed_verticle_lines_image = remove_verticle_lines(removed_horizontal_lines_image)
            cv2.imwrite('media/converted/cv6.png',removed_verticle_lines_image)

            #Conversion N
            # There are some more conversions 

            # skeletonize_image = skeletonize(removed_horizontal_lines_image)
            # cv2.imwrite('media/converted/cv7.png',skeletonize_image)

            denoise_image = denoise(removed_verticle_lines_image)
            cv2.imwrite('media/converted/cvN.png',denoise_image)

            #End of dummy conversions

            #Extracted data TODO: Improve performance
            ocr_text=str(pytesseract.image_to_string(removed_verticle_lines_image,lang='script/Devanagari'))

            #Bounded rectange
            bounded_rectangle_image = get_bounded_rectangles_on_identified_text(removed_verticle_lines_image)
            cv2.imwrite('media/converted/brres.png',bounded_rectangle_image)
            
    
            #Data formation : TODO: Improve code
            context['cv1_url'] = '/media/converted/cv1.png'
            context['cv2_url'] = '/media/converted/cv2.png'
            context['cv3_url'] = '/media/converted/cv3.png'
            context['cv4_url'] = '/media/converted/cv4.png'
            context['cv5_url'] = '/media/converted/cv5.png'
            context['cv6_url'] = '/media/converted/cv6.png'
            context['brres_url'] = '/media/converted/cv2.png'
            context['conversion_result'] = '/media/converted/brres.png'

    context['form'] = form
    return render(request,'rectex/rectex_template.html',context=context)

