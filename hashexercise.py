import bcrypt
import hashlib

def hash_pass():
    rawinput = input("please enter your password: ")
    salt = bcrypt.gensalt()
    print(f"the salt is {salt}")
    hashed = bcrypt.hashpw(rawinput.encode(),salt)
    print(f"the hashed password is {hashed}")
    return hashed.decode() #why decode?


# hashed = hash_pass()
# print(hashed)