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
def save_userDB(username, email, password, salt):
    conn = get_db_connection()
    cursor = conn.cursor()
    insert_user = "INSERT INTO users (username, email, hashed_password) VALUES (%s, %s, %s)"
    cursor.execute(insert_user, (username, email, password))
    user_id = cursor.lastrowid
    insert_salt = "INSERT INTO salts (ID, salt) VALUES (%s, %s)"
    cursor.execute(insert_salt, (user_id, salt))
    conn.commit()
    cursor.close()
    conn.close()

def hash_pass(password):
    password_bytes = password.encode()
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes,salt)
    return salt.decode(), hashed.decode()

def validate_user(username, password, email):
    errors = []

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    if cursor.fetchone():
        errors.append("Email already registered.")
    cursor.close()
    conn.close()
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
        email = data['email']
        salt, hashed_password = hash_pass(data['password'])
        save_userDB(username, email, hashed_password, salt)
    except Exception as e:
        print("Error in handle_register:", e)
        print(data)