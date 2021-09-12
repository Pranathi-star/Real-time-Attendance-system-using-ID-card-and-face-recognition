import numpy as np
import cv2
import pickle
from PIL import Image
import os
import pathlib

class FaceCapture(object):

    def detect_face(self):
        img = "app/faceshot0.png"
        face_cascade = cv2.CascadeClassifier("C:/Users/prana/OneDrive/Desktop/web_dev/ocr_trial/flask_cbit_smart_attendance/app/face_recognition_training_files/haarcascade_frontalface_alt2.xml")
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read("C:/Users/prana/OneDrive/Desktop/web_dev/ocr_trial/flask_cbit_smart_attendance/app/trainer.yml")

        labels = {"160119733136": 160119733136}
        filename = "/C:/Users/prana/OneDrive/Desktop/web_dev/ocr_trial/flask_cbit_smart_attendance/app/labels.pickle"
        HERE = pathlib.Path(__file__).parent
        with open(HERE/"labels.pickle", "rb") as f:
            og_labels = pickle.load(f)
            labels = {v:k for k,v in og_labels.items()}

        face_img = np.array(Image.open(img))
        face_img = cv2.resize(face_img, (450,450))
        gray = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
        face_rects = face_cascade.detectMultiScale(face_img)
        for (x,y,w,h) in face_rects:
            cv2.rectangle(face_img, (x,y), (x+w,y+h), (255,255,255), 5)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = face_img[y:y+h, x:x+w]

            id_, conf = recognizer.predict(roi_gray)
            
        if "id_" in locals():
            return labels[id_]
        else:
            return "Try Again"  
            