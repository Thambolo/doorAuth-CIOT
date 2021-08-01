import cv2
import numpy as np
import os
import requests
import mysql.connector as mysql

db = mysql.connect(
    host = "localhost",
    user = "root",
    passwd = "1qwer$#@!",
    database = "ep0403",
    port = 3306
)

cursor = db.cursor()

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer.yml')

face_cascade_Path = "haarcascade_frontalface_default.xml"


faceCascade = cv2.CascadeClassifier(face_cascade_Path)

font = cv2.FONT_HERSHEY_SIMPLEX

id = 0
# names related to ids: The names associated to the ids: 1 for Mohamed, 2 for Jack, etc...
names = ['None', 'JunDe'] # add a name into this list
#Video Capture
cam = cv2.VideoCapture(0)
cam.set(3, 640)
cam.set(4, 480)
# Min Height and Width for the  window size to be recognized as a face
minW = 0.1 * cam.get(3)
minH = 0.1 * cam.get(4)

authenticated = ""
count = 0

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
        if (confidence < 45):
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
        if count > 99:
            authenticated = "false"
    
    cv2.imshow('camera', img)
    # Escape to exit the webcam / program
    k = cv2.waitKey(10) & 0xff
    if k == 27:
        break

cam.release()
cv2.destroyAllWindows()

print(authenticated)
password = "12345"
if authenticated == "true":
    print("Uploading data to thingspeak...")
    requests.get('https://api.thingspeak.com/update?api_key=QDX9HH8L7R6QM5NF&field1=1')
else:
    guess = input("WHAT IS THE PASSWORD FOOLISH ONE!\n")
    if (guess == password):
        print("doors opening")
    else:
        print("password wrong")

print("\n [INFO] Exiting Program.")

