from django import forms
from .models import *

class ImageUpload(forms.ModelForm):
    class Meta:
        model = Id_Ocr
        fields = ['image']