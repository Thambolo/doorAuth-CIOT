import cv2
import numpy as np
import os
import requests
import mysql.connector as mysql
import datetime
import subprocess

from pathlib import Path
import cv2
import dlib
import numpy as np
import os
import argparse
from contextlib import contextmanager
from omegaconf import OmegaConf
from tensorflow.keras.utils import get_file
import subprocess
import glob

import sys
import argparse
import mysql.connector as mysql
import random
import requests #added

db = mysql.connect(
    host = "localhost",
    user = "root",
    passwd = "",
    database = "ep0403",
    port = 3307
)

cursor = db.cursor()

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer.yml')

face_cascade_Path = "haarcascade_frontalface_default.xml"


faceCascade = cv2.CascadeClassifier(face_cascade_Path)

font = cv2.FONT_HERSHEY_SIMPLEX

id = 0
# names related to ids: The names associated to the ids: 1 for Mohamed, 2 for Jack, etc...

names = ['None', 'JunDe','JunDe', 'JunDe'] # add a name into this list

#Video Capture
cam = cv2.VideoCapture(0)
cam.set(3, 640)
cam.set(4, 480)
# Min Height and Width for the  window size to be recognized as a face
minW = 0.1 * cam.get(3)
minH = 0.1 * cam.get(4)

authenticated = ""
count = 0


passwordlist = []

while (not authenticated):
    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(int(minW), int(minH)),
    )

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        id, confidence = recognizer.predict(gray[y:y + h, x:x + w])
        #print(confidence)
        if (confidence < 0):
            #print(names)
            id = names[0]
            confidence = "  {0}%".format(round(100 - confidence))
            #print(confidence)
            print("Authenticated")
            
            authenticated = "true"
        else:
            # Unknown Face
            count += 1
            print(count)
            id = "Who are you ?"
            confidence = "  {0}%".format(round(100 - confidence))

        cv2.putText(img, str(id), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
        cv2.putText(img, str(confidence), (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)
        if count > 10: #fail counter
            authenticated = "false"
    
    cv2.imshow('camera', img)
    # Escape to exit the webcam / program
    k = cv2.waitKey(10) & 0xff
    if k == 27:
        break

cam.release()
cv2.destroyAllWindows()

print(confidence)
print(authenticated)

if authenticated == "true":
    print("Uploading data to thingspeak...")
    requests.get('https://api.thingspeak.com/update?api_key=QDX9HH8L7R6QM5NF&field1=1')
else:
    query = "SELECT pin FROM passwd"
    cursor.execute(query)
    allpasswords = cursor.fetchall() ## it returns list of tables present in the
    length = len(allpasswords)
    for password in allpasswords:
        for passwd in password:
            passwordlist.append(passwd)

    failcount = 0

    while failcount < 2:
        guess = int(input("WHAT IS THE PASSWORD FOOLISH ONE!\n"))
        for i in passwordlist:
            if guess == i:
                failcount = 3
        failcount += 1

    print(failcount)

    if failcount == 2:
        print("password wrong")
        camera = cv2.VideoCapture(0)
        return_value, image = camera.read()
        timenow = datetime.datetime.now()
        dt_string = timenow.strftime("%d-%m-%Y_%H-%M-%S")
        print(dt_string)
        cv2.imwrite(f'../../yu4u_ageGender_ciot/dave_imgdir/Intruder-{dt_string}.jpg', image)
        del(camera)
        os.chdir('../../')
        cmd = f"python ./yu4u_ageGender_ciot/demo.py"
        
        process1= subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Calling ageGender...")
        print(process1.returncode)
        print(process1.stderr)
        print(process1.stdout)
    else:
        print("password correct")
        print("Uploading data to thingspeak...")
        requests.get('https://api.thingspeak.com/update?api_key=QDX9HH8L7R6QM5NF&field1=1')


print("\n [INFO] Exiting Program.")

