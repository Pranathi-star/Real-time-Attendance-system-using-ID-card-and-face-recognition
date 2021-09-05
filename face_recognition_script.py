import numpy as np
import cv2
import pickle
from PIL import Image


face_cascade = cv2.CascadeClassifier('face_recognition_training_files/haarcascade_frontalface_alt2.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainer.yml")

labels = {"160119733136": 160119733136}
with open("labels.pickle", "rb") as f:
     og_labels = pickle.load(f)
     labels = {v:k for k,v in og_labels.items()}

cam = cv2.VideoCapture(0)

cv2.namedWindow("Face capture")

img_counter = 0

while True:
    ret, frame = cam.read()
    if not ret:
        print("Failed to grab frame")
        break
    cv2.imshow("Face Capture", frame)

    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k%256 == 32:
        # SPACE pressed
        img_name = "face_recognition_gen_images/opencv_frame_{}.png".format(img_counter)
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        img_counter += 1

cam.release()

cv2.destroyAllWindows()

def detect_face(img):
    face_img = np.array(Image.open(img))
    face_img = cv2.resize(face_img, (450,450))
    gray = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
    face_rects = face_cascade.detectMultiScale(face_img,scaleFactor=1.2, minNeighbors=10)
    for (x,y,w,h) in face_rects:
        cv2.rectangle(face_img, (x,y), (x+w,y+h), (255,255,255), 5)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = face_img[y:y+h, x:x+w]

        id_, conf = recognizer.predict(roi_gray)
        # if conf>=50 and conf<=85:
        #     font = cv2.FONT_HERSHEY_PLAIN
        #     name = labels[id_]
        #     cv2.putText(face_img, name, (x, y-20), font, 1.5, (255, 255, 255), 2, cv2.LINE_AA)
        # else:
        #     cv2.rectangle(face_img, (x, y), (x + w, y + h), (0, 0, 255), 5)
        # img_item = "new.png"
        # cv2.imwrite(img_item, roi_color)
        
    if "id_" in locals():
        return labels[id_]
    else:
        return "Try Again"

print(detect_face(img_name))