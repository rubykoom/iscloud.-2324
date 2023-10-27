import mysql.connector
import json
import os
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, ISCloud!'

@app.route('/widgets')
def get_widgets():
    mydb = mysql.connector.connect(
        host="localhost",
        port=3316,
        user="root",
        password=os.environ.get('MYSQL_ROOT_PASSWORD'),
        # password = "p@ssw0rd1",
        database="inventory"
    )
    cursor = mydb.cursor()


    cursor.execute("SELECT * FROM widgets")

    row_headers=[x[0] for x in cursor.description] #this will extract row headers

    results = cursor.fetchall()
    json_data=[]
    for result in results:
        json_data.append(dict(zip(row_headers,result)))

    cursor.close()

    return json.dumps(json_data)

@app.route('/initdb')
def db_init():
    mydb = mysql.connector.connect(
        host="localhost",
        port=3316,
        user="root",
        password=os.environ.get('MYSQL_ROOT_PASSWORD')
        # password = "p@ssw0rd1",
    )
    cursor = mydb.cursor()

    cursor.execute("DROP DATABASE IF EXISTS inventory")
    cursor.execute("CREATE DATABASE inventory")
    cursor.close()

    mydb = mysql.connector.connect(
        host="localhost",
        port=3316,
        user="root",
        password=os.environ.get('MYSQL_ROOT_PASSWORD'),
        # password = "p@ssw0rd1",
        database="inventory"
    )
    cursor = mydb.cursor()

    cursor.execute("DROP TABLE IF EXISTS widgets")
    cursor.execute("CREATE TABLE widgets (name VARCHAR(255), description VARCHAR(255))")
    cursor.close()

    return 'init database'

if __name__ == "__main__":
    app.run(host ='0.0.0.0')