from django.db import models

# Create your models here.
class OCR(models.Model):
    #TODO: Add dummy user so that it can be associated with it
    to_be_converted_image = models.ImageField(upload_to='raw_images/')
