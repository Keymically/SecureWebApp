import mysql.connector
from os import getenv

from app import conn

# Create a cursor object
cursor = conn.cursor()

#example lets try some stuff
try:
    username = "fiona"
    password = "ogresAreLikeOnions"
    salt = "asdf123"
    insert_user = "INSERT INTO users (username, hashed_password) VALUES (%s, %s)"
    cursor.execute(insert_user, (username, password))
    user_id = cursor.lastrowid

    insert_salt = "INSERT INTO salts (ID, salt) VALUES (%s, %s)"
    cursor.execute(insert_salt, (user_id, salt))
    conn.commit()
    print(f"✅ User '{username}' added with ID {user_id}.")
except mysql.connector.Error as err:
    print("📛 Database error:", err)

#Fetch all users
cursor.execute("SELECT * FROM users")
results = cursor.fetchall()

for row in results:
    print(row)

# Don't forget to close!
cursor.close()
conn.close()