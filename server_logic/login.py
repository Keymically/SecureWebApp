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


def safe_base64_decode(encoded_str):

    if not isinstance(encoded_str, str):
        raise ValueError("Expected a base64-encoded string.")

    padded_str = encoded_str + '=' * (-len(encoded_str) % 4)
    return base64.b64decode(padded_str)

def verify_pass_with_hmac(password, salt_b64, hmac_b64):

    try:
        salt = safe_base64_decode(salt_b64)
        stored_hmac = safe_base64_decode(hmac_b64)

        password_bytes = password.encode()
        computed_hmac = hmac.new(
            key=HMAC_SECRET_KEY,
            msg=password_bytes + salt,
            digestmod=hashlib.sha256
        ).digest()

        return hmac.compare_digest(computed_hmac, stored_hmac)

    except (base64.binascii.Error, ValueError) as e:
        print(f"[verify_pass_with_hmac] Decoding error: {e}")
        return False

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