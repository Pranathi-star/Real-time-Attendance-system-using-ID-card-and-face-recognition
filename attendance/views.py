from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
import base64
import random
import string
from .models import *
from django.http import JsonResponse

@csrf_exempt
def index(request):
    if request.method == "POST":
        print(1)
        data = request.body
        data = json.loads(data[0:len(data)])
        temp = len('data:image/jpeg;base64,')
        for d in data:
            d = d[temp:len(d)]
            imgdata = base64.b64decode(d)  
            filename = "object_recognition_gen_images/opencv_frame_0.png"
            with open(filename, 'wb') as f:
                f.write(imgdata)
            i = Id_Ocr.objects.create(file=filename)
            i.save()
        return JsonResponse({'data': 'Success'})
    return render(request, 'index.html')
