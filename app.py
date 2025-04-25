import os

import sqlalchemy
from flask import Flask, render_template, send_from_directory, request, jsonify
import mysql.connector
from os import getenv

import hashexercise

# Connect to the database
conn = mysql.connector.connect(
    host=getenv('DB_HOST'),
    user=getenv('DB_USER'),
    password=getenv('DB_PASS'),
    database=getenv('DB_DBNAME')
)

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return send_from_directory(".", path="pages/index.html")

@app.route('/register')
def register():
    # hashexercise.hash_pass() #when user is registering we will hash with salt and store the hashed result in the DB
    return send_from_directory(".", path="pages/registerPage.html")
@app.route('/changePassword')
def changePassword():
    return send_from_directory(".", path="pages/changePassword.html")
@app.route('/login')
def login():
    # hashexercise.hash_pass() #when someone tries to login we need to hash the password with his own salt from the DB to check if the password is correct

    return send_from_directory(".", path="pages/loginPage.html")
@app.route('/systemScreen')
def systemScreen():
    return '<h1>System Screen... whatever that means</h1>'
@app.route('/forgotPassword')
def forgotPassword():
    return '<h1>How did you forget your password we havn\'t even implemented those</h1>'

@app.route('/api/login', methods=['POST'])
def apilogin():
    data = request.get_json()  # parse JSON body

    username = data.get('username')
    password = data.get('password')
    print(username + " " + password)

    if username == "admin" and password == "1234":
        return jsonify({ "success": True, "message": "Logged in!" }), 200
    else:
        return f"<h3> {username} is here!!</h3>"
        # return jsonify({ "success": False, "message": "Invalid credentials" }), 401



if __name__ == '__main__':
    app.run()
