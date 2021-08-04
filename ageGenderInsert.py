import sys
import argparse
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
def get_args():
    parser = argparse.ArgumentParser(description="This script detects faces from web cam input, "
                                                 "and estimates age and gender for the detected faces.",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--age", type=str, default=None,
                        help="age given by demo.py")
    parser.add_argument("--gender", type=str, default=None,
                        help="gender given by demo.py")
    parser.add_argument("--imageDir", type=str, default=None,
                        help="directory of image demo.py")
    args = parser.parse_args()
    return args
args= get_args()

## tweeter
tweetApiKey = "Z57OA2M6UVW36FGR" #add our own key

## get ML data age and gender
age = args.age#random.randrange(16,50) #sys.argv[1]
#genderList = ['male','female']
gender = args.gender#random.choice(genderList) #sys.argv[2]
imageDir = args.imageDir

now = datetime.now()
current_time = now.strftime("%d/%m/%Y, %H:%M:%S")

ageRange = f"{int(age)-4}-{int(age)+4}"

requests.post('https://api.thingspeak.com/apps/thingtweet/1/statuses/update',
            json={'api_key':tweetApiKey,'status':'ALERT: Possible Intruder!\nTime: {time}\nGender: {g}\nAge: {a}'.format(time=current_time,g=gender,a=ageRange)})

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

