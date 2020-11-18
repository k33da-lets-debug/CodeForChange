from django.forms import ModelForm
from .models import OCR

# Create the form class.
class OCRForm(ModelForm):
    class Meta:
        model = OCR
        fields = ['to_be_converted_image']