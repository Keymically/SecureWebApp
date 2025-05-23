import os
from flask import Flask, render_template, send_from_directory, request, jsonify
import mysql.connector
from os import getenv
from dotenv import load_dotenv
import bcrypt
import hashlib
from email.mime.text import MIMEText
import smtplib
import random
import string
from server_logic import apiRegister
from server_logic import login as APIlogin

#test
load_dotenv()
app = Flask(__name__)
def get_db_connection():
    return mysql.connector.connect(
        host=getenv('DB_HOST'),
        user=getenv('DB_USER'),
        password=getenv('DB_PASS'),
        database=getenv('DB_DBNAME'),
        use_pure=True
    )

@app.route('/')
def hello_world():  # put application's code here
    return send_from_directory(".", path="pages/index.html")

@app.route('/click')
def click():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(results)
@app.route('/click2')
def click2():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM salts")
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(results)
@app.route('/register')
def register():
    #hashexercise.hash_pass() #when user is registering we will hash with salt and store the hashed result in the DB
    return send_from_directory(".", path="pages/registerPage.html")
@app.route('/changePassword')
def changePassword():
    return send_from_directory(".", path="pages/changePassword.html")
@app.route('/login')
def login():
    return send_from_directory(".", path="pages/loginPage.html")

@app.route('/systemScreen')
def systemScreen():
    return send_from_directory(".", path="pages/systemScreen.html")
@app.route('/add_customer', methods=['POST'])
def add_customer():
    data = request.get_json()
    first_name = data.get('firstName')
    last_name = data.get('lastName')
    phone = data.get('phone')
    bday = data.get('bday')
    email = data.get('email')

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO customers (first_name, last_name, phone_number, birth_date, email)
            VALUES (%s, %s, %s, %s, %s)
        ''', (first_name, last_name, phone, bday, email))
        conn.commit()
        return jsonify({'message': 'Customer added successfully'}), 201
    except mysql.connector.Error as err:
        print('DB Error:', err)
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/customers')
def get_customers():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM customers')
    customers = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(customers)
@app.route('/forgotPassword')
def forgotPassword():
    return send_from_directory(".", path="pages/forgot_password.html")

def send_email(to_email, token):
    msg = MIMEText(f'Your reset token is: {token}')
    msg['Subject'] = 'Password Reset'
    msg['From'] = 'your_email@gmail.com'
    msg['To'] = to_email

    with smtplib.SMTP('sandbox.smtp.mailtrap.io', 587) as smtp:
        smtp.starttls()
        smtp.login('8637650889cca2', 'b5e3fa51a408a8')
        smtp.send_message(msg)

@app.route('/forgot-password', methods=['POST'])
def forgot_password():
    username = request.json.get('username')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM users WHERE email = %s', (username,))
    user = cursor.fetchone()

    if not user:
        return jsonify({'error': 'User not found'}), 404


    raw_token = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
    token = hashlib.sha1(raw_token.encode()).hexdigest()

    cursor.execute('UPDATE users SET reset_token = %s, token_created_at = NOW() WHERE ID = %s',
                   (token, user['ID']))
    conn.commit()
    cursor.close()
    conn.close()

    # Send token to email (simulate or actually send)
    send_email(username, token)  # assuming username is the email

    return jsonify({'message': 'Reset token sent to your email'}), 200

@app.route('/verify-token', methods=['POST'])
def verify_token():
    username = request.json.get('username')
    token = request.json.get('token')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM users WHERE email = %s AND reset_token = %s', (username, token))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if user:
        return jsonify({'message': 'Token valid. Proceed to reset password'}), 200
    else:
        return jsonify({'error': 'Invalid token'}), 400

@app.route('/reset-password', methods=['POST'])
def reset_password():
    username = request.json.get('username')
    token = request.json.get('token')
    new_password = request.json.get('newPassword')

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE email = %s AND reset_token = %s', (username, token))
    user = cursor.fetchone()
    if not user:
        return jsonify({'error': 'Invalid token'}), 400

    hashed_pw = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()

    cursor.execute('UPDATE users SET hashed_password = %s, reset_token = NULL, token_created_at = NULL WHERE email = %s',
                   (hashed_pw, username))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'message': 'Password updated successfully'}), 200
@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Missing JSON payload'}), 400

    email = data.get('username')
    password = data.get('password')
    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    credentials = APIlogin.get_credentials_by_email(email)
    if not credentials:
        return jsonify({'error': 'Invalid email or password'}), 401

    stored_hash, stored_salt = credentials
    if not APIlogin.verify_pass_with_hmac(password, stored_salt, stored_hash):
        return jsonify({'error': 'Invalid email or password'}), 401

    return jsonify({'message': 'Login successful'}), 200

@app.route('/api/register', methods=['POST'])
def api_register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    errors = apiRegister.validate_user(username, password, email)
    if errors:
        return jsonify({"success": False, "errors": errors}), 400

    apiRegister.handle_register(data)

    return jsonify({"success": True, "message": f"Welcome, {username}!"}), 200
if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
