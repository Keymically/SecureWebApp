import bcrypt
import mysql.connector
from os import getenv
import hmac
import hashlib
import base64
from server_logic.utils import *
from dotenv import load_dotenv

load_dotenv()
HMAC_SECRET_KEY = getenv('HMAC_SECRET_KEY')
if HMAC_SECRET_KEY is None:
    raise ValueError("HMAC_SECRET_KEY is not set in environment variables.")

HMAC_SECRET_KEY = HMAC_SECRET_KEY.encode()


def get_db_connection():
    return mysql.connector.connect(
        host=getenv('DB_HOST'),
        user=getenv('DB_USER'),
        password=getenv('DB_PASS'),
        database=getenv('DB_DBNAME'),
        use_pure=True
    )
def save_userDB(username, email, hashed_password, salt):
    conn = get_db_connection()
    cursor = conn.cursor()
    insert_user = """
            INSERT INTO users (username, email, hashed_password)
            VALUES (%s, %s, %s)
        """
    cursor.execute(insert_user, (username, email, hashed_password))
    user = get_user_from_table(cursor,email)
    if user is None:
        raise ValueError("User not found")
    user_id = user[0]

    insert_salt = """
        INSERT INTO salts (ID, salt)
        values (%s, %s)
    """

    cursor.execute(insert_salt, (user_id, salt))
    conn.commit()
    cursor.close()
    conn.close()


def hash_pass_with_hmac(password):
    salt = bcrypt.gensalt()
    password_bytes = password.encode()

    hmac_hash = hmac.new(HMAC_SECRET_KEY, password_bytes + salt, hashlib.sha256).digest()

    return base64.b64encode(salt).decode(), base64.b64encode(hmac_hash).decode()


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
        salt, hashed_password = hash_pass_with_hmac(data['password'])
        save_userDB(username, email, hashed_password, salt)
    except Exception as e:
        print("Error in handle_register:", e)
        print(data)