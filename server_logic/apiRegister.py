import bcrypt
import hashlib


def save_userDB(username,password,salt):
    from app import conn
    cursor = conn.cursor()
    #Open Connection
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

def handle_register(data):
    try:
        username = data['username']
        salt, password = hash_pass(data['password'])
        save_userDB(username,password,salt)
    except:
        print(data)