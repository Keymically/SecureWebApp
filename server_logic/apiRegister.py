import bcrypt
import mysql.connector
from password_strength import PasswordPolicy
from os import getenv
from server_logic.utils import *

def get_db_connection():
    return mysql.connector.connect(
        host=getenv('DB_HOST'),
        user=getenv('DB_USER'),
        password=getenv('DB_PASS'),
        database=getenv('DB_DBNAME'),
        use_pure=True
    )
def save_userDB(username,password,salt):
    conn = get_db_connection()
    cursor = conn.cursor()
    insert_user = "INSERT INTO users (username, hashed_password) VALUES (%s, %s)"
    cursor.execute(insert_user, (username, password))
    user_id = cursor.lastrowid
    insert_salt = "INSERT INTO salts (ID, salt) VALUES (%s, %s)"
    cursor.execute(insert_salt, (user_id, salt))
    conn.commit()
    #close connection
    cursor.close()
    conn.close()

def hash_pass(password):
    password_bytes = password.encode()
    salt = bcrypt.gensalt()
    #print(f"the salt is {salt}")
    hashed = bcrypt.hashpw(password_bytes,salt)
    #print(f"the hashed password is {hashed}")
    return salt.decode(), hashed.decode()

def validate_user(username, password):
    errors = []

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    if result:
        errors.append("Username already exists.")

    password_policy, _ = get_password_policy()
    rules_messages = get_config_rules_messages()
    failed_rules = password_policy.test(password)

    for issue in failed_rules:
        name, number = str(issue).split("(")
        number = number.replace(")", "")
        errors.append(f"Password must have at least {number} {rules_messages[name]}")

    return errors

def handle_register(data):
    try:
        username = data['username']
        salt, password = hash_pass(data['password'])
        save_userDB(username,password,salt)
    except:
        print(data)