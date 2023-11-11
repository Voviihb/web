import mysql.connector

dataBase = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="123456"
)

# preparing a cursor object
cursorObject = dataBase.cursor()

# creating database
cursorObject.execute("CREATE DATABASE my_db CHARACTER SET utf8")