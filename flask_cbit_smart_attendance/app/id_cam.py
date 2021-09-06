import pixellib
from pixellib.instance import instance_segmentation
import numpy as np 
import matplotlib.pyplot as plt
from PIL import Image
import cv2
import pytesseract
from pytesseract import Output
import csv

class IdCapture(object):
    def ocr_of_captured_image(self, image):
        #converting image into gray scale image
        # gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        #  # converting it to binary image by Thresholding

        #  # this step is require if you have colored image because if you skip this part
        #  # then tesseract won't able to detect text correctly and this will give incorrect result
        
        # threshold_img = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        # display image
        # cv2.imshow('threshold image', threshold_img)
        # Maintain output window until user presses a key
        cv2.waitKey(0)
        # Destroying present windows on screen
        cv2.destroyAllWindows()

        #configuring parameters for tesseract
        custom_config = r'--oem 3 --psm 6'
        # now feeding image to tesseract
        details = pytesseract.image_to_data(image, output_type=Output.DICT, config=custom_config, lang='eng')
        # print(details.keys())

        total_boxes = len(details['text'])
        for sequence_number in range(total_boxes):
            if int(float(details['conf'][sequence_number])) >30:
                (x, y, w, h) = (details['left'][sequence_number], details['top'][sequence_number], details['width'][sequence_number],  details['height'][sequence_number])
                image = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # display image
        # cv2.imshow('captured text', threshold_img)
        # Maintain output window until user presses a key
        cv2.waitKey(0)
        # Destroying present windows on screen
        cv2.destroyAllWindows()

        parse_text = []
        word_list = []
        last_word = ''
        res = ''
        for word in details['text']:
            if word!='':
                word_list.append(word)
                last_word = word
            if (last_word!='' and word == '') or (word==details['text'][-1]):
                parse_text.append(word_list)
                word_list = []

        print(parse_text)
        # with open('result_text.txt',  'w', newline="") as file:
        #     csv.writer(file, delimiter=" ").writerows(parse_text)
        for sentence in parse_text:
            for word in sentence:
                if "1601" in word:
                    res = word
                    break
        return(res)

    def get_id_image(self):
        cam = cv2.VideoCapture(0)
        #resize frame
        cv2.namedWindow("ID Card Capture")
        img_counter = 0
        ret, frame = cam.read()
        # img_name = cv2.resize(frame, None, fx = ds_factor, fy = ds_factor, interpolation = cv2.INTER_AREA)
        if ret:
            img_name = cv2.resize(frame, (500, 500))
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

            # plt.title('threshold')
            # plt.subplot(1,3,3)
            xx = [contour[maxa_ind][i][0][0] for i in range(len(contour[maxa_ind]))]
            yy = [contour[maxa_ind][i][0][1] for i in range(len(contour[maxa_ind]))]

            #storing output for method 3

            roi = img_name[min(xx): min(xx) + max(xx), min(yy): min(yy) + max(yy)]
            # cv2.imwrite('object_detection_gen_images/Image_crop.jpg', roi)
            # image = cv2.imread("C:/Users/prana/OneDrive/Desktop/web_dev/ocr_trial/object_detection_gen_images/Image_crop.jpg")

            # plt.figure()
            # plt.imshow(img_name)
            # plt.plot(xx,yy,'r',linewidth=3)
            # plt.show()
            # plt.title('largest contour')

            # storing output for methods 1 and 2

            # Output to files
            # roi=img_name[y:y+h,x:x+w]
            ret, jpeg = cv2.imencode('.jpg', roi)

            # image = cv2.imread("C:/Users/prana/OneDrive/Desktop/web_dev/ocr_trial/Image_crop.jpg")

            roll_num = self.ocr_of_captured_image(roi)
            return jpeg.tobytes(), roll_num
                    
        if not ret:
            print("failed to grab frame")

            # cv2.imshow("ID Card Capture", frame)
            # img_name = "object_detection_gen_images/opencv_frame_{}.png".format(img_counter)
            # cv2.imwrite(img_name, frame)
            # print("{} written!".format(img_name))
            # img_counter += 1

            # cam.release()

            # cv2.destroyAllWindows()

            #Preprocessing image to be read
            