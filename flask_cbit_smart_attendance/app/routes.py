from flask import render_template, Response, redirect, flash, request, url_for
# from app import app, db, mail
from app.id_cam import IdCapture
# from app.models import User
# from werkzeug.urls import url_parse
import time
from datetime import datetime
# from flask_mail import Message
# import sqlite3
# import smtplib, ssl
# from email.message import EmailMessage
from app import app
res = 0
import cv2
import os

camera = cv2.VideoCapture(0)  # use 0 for web camera
global capture, switch 
capture=0
switch=1

@app.route('/') 
@app.route('/index')
def index():
    return render_template('index.html')

def gen():
    global capture
    while True:
        # Capture frame-by-frame
        success, frame = camera.read()  # read the camera frame
        if not success:
            pass
        else:
            if(capture):
                capture=0
                p = "shot0.png"
                cv2.imwrite(p, frame)
            try:
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result
            except Exception as e:
                pass


@app.route('/video_feed')
def video_feed():
    return Response(gen(), mimetype = 'multipart/x-mixed-replace; boundary=frame')

@app.route('/success')
def success():
    # current_user.wearing_mask = maskTF 
    # current_user.date_time = curr_datetime
    # db.session.commit()
    return render_template('success.html', res = res)

@app.route('/check')
def check():
    return render_template('id_capture.html')
 
@app.route('/requests',methods=['POST','GET'])
def tasks():
    global switch,camera
    if request.method == 'POST':
        if request.form.get('click') == 'Capture':
            global capture
            capture = 1
            return render_template('id_capture.html')
            
    elif request.method=='GET':
        return render_template('index.html')
    return render_template('index.html')

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', debug=True)