import mysql.connector as mysql

db = mysql.connect(
    host = "localhost",
    user = "root",
    passwd = "",
    database = "ep0403",
    port = 3307
)

cursor = db.cursor()
passwordlist = []


## getting all the tables which are present in ‘ep0403’ database
query = "SELECT pin FROM passwd"

cursor.execute(query)

allpasswords = cursor.fetchall() ## it returns list of tables present in the

length = len(allpasswords)

for password in allpasswords:
    for passwd in password:
        passwordlist.append(passwd)

failcount = 0

while failcount < 2:
    guess = int(input("password? : "))
    for i in passwordlist:
        if guess == i:
            failcount = 3
    failcount += 1

print(failcount)

if failcount == 2:
    print("password wrong")
else:
    print("password correct")
print("end")






