from django.db import models

# Create your models here.
class Id_Ocr(models.Model):
    file = models.ImageField()

    def __str__(self):
        return self.file