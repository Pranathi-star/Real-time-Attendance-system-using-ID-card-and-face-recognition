from flask import render_template, Response, redirect, flash, request, url_for
from app.id_cam import IdCapture
from app.face_cam import FaceCapture
import time
from datetime import datetime
from app import app
res = 0
import cv2
import os

camera = cv2.VideoCapture(0)
global capture, switch 
capture=0
switch=1
roll_num1 = 0
roll_num2 = 0

@app.route('/') 
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/check_id')
def check_id():
    return render_template('id_capture.html')
 
@app.route('/id_requests',methods=['POST','GET'])
def id_save():
    global switch,camera
    if request.method == 'POST':
        if request.form.get('click') == 'Capture':
            global capture
            capture = 1
            return render_template('id_capture.html')
            
    elif request.method=='GET':
        return render_template('index.html')
    return render_template('index.html')

def gen_id():
    global capture
    while True:
        # Capture frame-by-frame
        success, frame = camera.read()
        if not success:
            pass
        else:
            if(capture):
                capture=0
                p = "app/idshot0.png"
                cv2.imwrite(p, frame)
            try:
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result
            except Exception as e:
                pass

@app.route('/video_feed_id')
def video_feed_id():
    return Response(gen_id(), mimetype = 'multipart/x-mixed-replace; boundary=frame')

@app.route('/success_id')
def success_id():
    image = cv2.imread("C:/Users/prana/OneDrive/Desktop/web_dev/ocr_trial/flask_cbit_smart_attendance/app/idshot0.png")
    Id = IdCapture()
    global roll_num1
    roll_num1 = Id.get_id_image(image)
    return render_template('success1.html', res = roll_num1)

@app.route('/check_face')
def check_face():
    return render_template('face_capture.html')

@app.route('/face_requests',methods=['POST','GET'])
def face_save():
    global switch,camera
    if request.method == 'POST':
        if request.form.get('click') == 'Capture':
            global capture
            capture = 1
            return render_template('face_capture.html')
            
    elif request.method=='GET':
        return render_template('index.html')
    return render_template('index.html')

def gen_face():
    global capture
    while True:
        # Capture frame-by-frame
        success, frame = camera.read()
        if not success:
            pass
        else:
            if(capture):
                capture=0
                p = "app/faceshot0.png"
                cv2.imwrite(p, frame)
            try:
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result
            except Exception as e:
                pass

@app.route('/video_feed_face')
def video_feed_face():
    return Response(gen_face(), mimetype = 'multipart/x-mixed-replace; boundary=frame')

@app.route('/success_face')
def success_face():
    # image = cv2.imread("C:/Users/prana/OneDrive/Desktop/web_dev/ocr_trial/flask_cbit_smart_attendance/faceshot0.png")
    Face = FaceCapture()
    global roll_num2
    roll_num2 = Face.detect_face()
    return render_template('success2.html', res = str(roll_num1) + "," + str(roll_num2))