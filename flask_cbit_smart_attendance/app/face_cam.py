import numpy as np
import cv2
import pickle
from PIL import Image
import os
import pathlib

class FaceCapture(object):
    def train_face(self):
        face_cascade = cv2.CascadeClassifier('face_recognition_training_files/haarcascade_frontalface_alt2.xml')

        recognizer = cv2.face.LBPHFaceRecognizer_create()

        BASE_DIR =  os.path.dirname(os.path.abspath(__file__))
        image_dir = os.path.join(BASE_DIR, "face_recognition_training_data")

        current_id = 0
        label_ids = {}
        y_labels = []
        x_train = []

        for root, dirs, files in os.walk(image_dir):
            for file in files:
                if file.endswith("png") or file.endswith("jpeg"):
                    path = os.path.join(root, file)
                    label = os.path.basename(root).replace(" ","-").lower()
                    print(label, path)
                    if not label in label_ids:
                        label_ids[label] = current_id
                        current_id +=1

                    id_ = label_ids[label]
                    print(label_ids)
                    #y_labels.append(label)
                    #x_train.append(path)
                    pil_image = Image.open(path).convert("L")
                    image_array = np.array(pil_image, "uint8")
                    #print(image_array)
                    faces = face_cascade.detectMultiScale(image_array,scaleFactor=1.2, minNeighbors=10)

                    for(x,y,w,h) in faces:
                        roi = image_array[y:y+h, x:x+w]
                        x_train.append(roi)
                        y_labels.append(id_)
                        
        with open("labels.pickle", "wb") as f:
            pickle.dump(label_ids, f)

        recognizer.train(x_train, np.array(y_labels))
        recognizer.save("trainer.yml")

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
            