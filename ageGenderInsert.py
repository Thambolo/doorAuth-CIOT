import mysql.connector as mysql
import random
from datetime import datetime
import requests #added
db = mysql.connect(
port = 3307,
host = "localhost",
user = "root",
passwd = "",
database = "ep0403"
)
## tweeter
tweetApiKey = "Z57OA2M6UVW36FGR" #add our own key

## get ML data age and gender
age = random.randrange(16,50)
genderList = ['male','female']
gender = random.choice(genderList)
imageDir = "/yu4u_ageGender_ciot/dave_imgdir/img1.jpg"

now = datetime.now()
current_time = now.strftime("%d/%m/%Y, %H:%M:%S")
requests.post('https://api.thingspeak.com/apps/thingtweet/1/statuses/update',
            json={'api_key':tweetApiKey,'status':'ALERT: Possible Intruder!\nTime: {time}\nGender: {g}\nAge: {a}'.format(time=current_time,g=gender,a=age)})

cursor = db.cursor()
## defining the Query
query = "INSERT INTO predictions (age, gender, imageDir) VALUES (%s, %s, %s)"
## storing values in a variable
values = (age, gender,imageDir)
## executing the query with values
cursor.execute(query, values)
## to make final output we have to run the 'commit()' method of the database object
db.commit()
print(cursor.rowcount, "row, Gender:{gender} Age:{age} inserted".format(gender=gender,age=age))

