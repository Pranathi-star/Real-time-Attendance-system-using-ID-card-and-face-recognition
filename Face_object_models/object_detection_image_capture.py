import cv2
import pixellib
from pixellib.instance import instance_segmentation
import numpy as np 
import matplotlib.pyplot as plt
from PIL import Image
from object_detection_ocr import *
cam = cv2.VideoCapture(0)

cv2.namedWindow("ID Card Capture")

img_counter = 0

while True:
    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")
        break
    cv2.imshow("ID Card Capture", frame)

    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k%256 == 32:
        # SPACE pressed
        img_name = "object_detection_gen_images/opencv_frame_{}.png".format(img_counter)
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
# plt.figure()
# plt.imshow(threshold)
# plt.show()

contour_1 = img_name.copy()
contour, hierarchy = cv2.findContours(threshold,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(contour_1, contour,-1,(0,255,0),3)
# plt.figure()
# plt.imshow(contour_1)
# plt.show()

#method 1 to get the largest contour area 

# mx = (0,0,0,0)      # biggest bounding box so far
# mx_area = 0
# for cont in contour:
#     x,y,w,h = cv2.boundingRect(cont)
#     area = w*h
#     if area > mx_area:
#         mx = x,y,w,h
#         mx_area = area


# method 2 to get largest contour area

# c = max(contour, key = cv2.contourArea)
# # x,y,w,h = mx
# x, y, w, h = cv2.boundingRect(c)


#method 3 to get largest contour area

area = np.array([cv2.contourArea(contour[i]) for i in range(len(contour))]) #list of all areas
maxa_ind = np.argmax(area) # index of maximum area contour

plt.title('threshold')
plt.subplot(1,3,3)
xx = [contour[maxa_ind][i][0][0] for i in range(len(contour[maxa_ind]))]
yy = [contour[maxa_ind][i][0][1] for i in range(len(contour[maxa_ind]))]

#storing output for method 3

roi = img_name[min(xx): min(xx) + max(xx), min(yy): min(yy) + max(yy)]
cv2.imwrite('object_detection_gen_images/Image_crop.jpg', roi)
image = cv2.imread("C:/Users/prana/OneDrive/Desktop/web_dev/ocr_trial/object_detection_gen_images/Image_crop.jpg")

# plt.figure()
# plt.imshow(img_name)
# plt.plot(xx,yy,'r',linewidth=3)
# plt.show()
# plt.title('largest contour')

# storing output for methods 1 and 2

# Output to files
# roi=img_name[y:y+h,x:x+w]
# cv2.imwrite('Image_crop.jpg', roi)

# image = cv2.imread("C:/Users/prana/OneDrive/Desktop/web_dev/ocr_trial/Image_crop.jpg")

ocr_of_captured_image(image)
