from django.db import models
from .form_utils import validate_image

# Create your models here.
class OCR(models.Model):
    #TODO: We can add users associated with it in further versions
    to_be_converted_image = models.ImageField(upload_to='raw_images/',validators=[validate_image])
