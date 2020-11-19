from django.shortcuts import render,redirect
from django.http import HttpResponse
from PIL import Image
import pytesseract
import cv2
import numpy as np
from .image_transformation_utils import (compute_skew,deskew,skeletonize,
                                        remove_noise,remove_lines,remove_horizontal_lines,
                                        remove_verticle_lines,get_bounded_rectangles_on_identified_text,
                                        denoise,)
from .forms import OCRForm
from .models import OCR
from .export_utils import extractCoordsData,convertToExel

# Created by Ninad Parab(k33da_the_bug)
def rectex_view(request):

    context = {}
    form = OCRForm() 

    form = OCRForm()
    if request.method == 'POST':
        form = OCRForm(request.POST,request.FILES)
        if form.is_valid():
            d=form.save()
            
            #Image preprocessing pipeline
            data = OCR.objects.get(id=d.id)
            url = data.to_be_converted_image.url[1:]
            file_meta =url.split('/')[-1]
            filename = file_meta.split('.')[0]

            raw_image = Image.open(url)
            opencv_image = cv2.cvtColor(np.array(raw_image), cv2.COLOR_RGB2BGR)
            
            #conversion 1
            rgb_image = cv2.cvtColor(opencv_image,cv2.COLOR_BGR2RGB)
            tempu = 'media/converted/'+filename+'_'+'cv1.png'
            context['cv1_url'] = tempu
            cv2.imwrite(tempu,rgb_image)
            
            #Conversion 2
            grayscale_image = cv2.cvtColor(rgb_image,cv2.COLOR_RGB2GRAY)
            tempu = 'media/converted/'+filename+'_'+'cv2.png'
            context['cv2_url'] = tempu
            cv2.imwrite(tempu,grayscale_image)
            
            #Conversion 3
            binary_image = cv2.threshold(grayscale_image, 128, 255, cv2.THRESH_BINARY)[1] 
            tempu = 'media/converted/'+filename+'_'+'cv3.png'
            context['cv3_url'] = tempu
            cv2.imwrite(tempu,binary_image)

            #Conversion 4
            kernel = np.ones((2,2), np.uint8) 
            text_thickned_image = cv2.erode(binary_image,kernel,iterations = 1)
            tempu = 'media/converted/'+filename+'_'+'cv4.png'
            context['cv4_url'] = tempu
            cv2.imwrite(tempu,text_thickned_image)

            #Conversion 5
            removed_horizontal_lines_image = remove_horizontal_lines(text_thickned_image)
            tempu = 'media/converted/'+filename+'_'+'cv5.png'
            context['cv5_url'] = tempu
            cv2.imwrite(tempu,removed_horizontal_lines_image)

            #Conversion 6
            removed_verticle_lines_image = remove_verticle_lines(removed_horizontal_lines_image)
            tempu = 'media/converted/'+filename+'_'+'cv6.png'
            context['cv6_url'] = tempu
            cv2.imwrite(tempu,removed_verticle_lines_image)

            #Conversion N (Not used)
            # There are some more conversions 

            # skeletonize_image = skeletonize(removed_horizontal_lines_image)
            # cv2.imwrite('media/converted/cv7.png',skeletonize_image)

            # denoise_image = denoise(removed_verticle_lines_image)
            # cv2.imwrite('media/converted/cvN.png',denoise_image)

            # End of dummy conversions

            # Extracted data TODO: Improve performance by eliminating images
            ocr_text=str(pytesseract.image_to_string(removed_verticle_lines_image,lang='script/Devanagari',config='--oem 3 --psm 6'))
            context['result'] = ocr_text

            #Bounded rectange result
            bounded_rectangle_image = get_bounded_rectangles_on_identified_text(removed_verticle_lines_image)
            tempu = 'media/converted/'+filename+'_'+'brres.png'
            context['conversion_result'] = tempu
            cv2.imwrite(tempu,bounded_rectangle_image)

            context['result_flag'] = True

            # Exel functionality
            # extracted_coords = extractCoordsData(removed_verticle_lines_image)
            # tempu = 'media/exel/'+filename+'_output.xlsx'
            # exportxl_data = convertToExel(extracted_coords)
            # exportxl_data.to_excel(tempu,sheet_name='Sheet_name_1')
            
            # context['exel_sheet'] = tempu
            
    
    context['form'] = form
    return render(request,'rectex/rectex_template.html',context=context)


