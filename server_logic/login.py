import bcrypt
import mysql.connector
from os import getenv
from server_logic.utils import *
import hmac
import hashlib
import base64
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


def verify_pass_with_hmac(password, stored_salt_b64, stored_hmac_b64):
    salt = base64.b64decode(stored_salt_b64)
    stored_hmac = base64.b64decode(stored_hmac_b64)

    password_bytes = password.encode()
    computed_hmac = hmac.new(HMAC_SECRET_KEY, password_bytes + salt, hashlib.sha256).digest()

    return hmac.compare_digest(computed_hmac, stored_hmac)

def get_credentials_by_email(email):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT u.hashed_password, s.salt
        FROM users u
        JOIN salts s ON u.id = s.id
        WHERE u.email = %s
    """
    cursor.execute(query, (email,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result