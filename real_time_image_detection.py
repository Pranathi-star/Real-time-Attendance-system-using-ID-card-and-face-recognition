import cv2
import pixellib
from pixellib.instance import instance_segmentation
import numpy as np 
import matplotlib.pyplot as plt
from PIL import Image
from ocr_of_uploaded_image import *
cam = cv2.VideoCapture(0)

cv2.namedWindow("test")

img_counter = 0

while True:
    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")
        break
    cv2.imshow("test", frame)

    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k%256 == 32:
        # SPACE pressed
        img_name = "opencv_frame_{}.png".format(img_counter)
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        img_counter += 1

cam.release()

cv2.destroyAllWindows()

img_name = np.array(Image.open(img_name))
#Preprocessing image to be read
img_name = cv2.resize(img_name, (450,450))
# function to greyscale, blur and change the receptive threshold of image
def preprocess(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 
    blur = cv2.GaussianBlur(gray, (3,3),6) 
    #blur = cv2.bilateralFilter(gray,9,75,75)
    threshold_img = cv2.adaptiveThreshold(blur,255,1,1,11,2)
    return threshold_img

threshold = preprocess(img_name)
#let's look at what we have got
plt.figure()
# plt.imshow(threshold)
# plt.show()

contour_1 = img_name.copy()
contour, hierarchy = cv2.findContours(threshold,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(contour_1, contour,-1,(0,255,0),3)
#let's see what we got
mx = (0,0,0,0)      # biggest bounding box so far
mx_area = 0
for cont in contour:
    x,y,w,h = cv2.boundingRect(cont)
    area = w*h
    if area > mx_area:
        mx = x,y,w,h
        mx_area = area
x,y,w,h = mx

# Output to files
roi=img_name[y:y+h,x:x+w]
cv2.imwrite('Image_crop.jpg', roi)

image = cv2.imread("C:/Users/prana/OneDrive/Desktop/web_dev/ocr_trial/Image_crop.jpg")

ocr_of_captured_image(image)
