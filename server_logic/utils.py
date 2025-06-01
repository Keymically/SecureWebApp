from password_strength import PasswordPolicy
import json

def get_password_policy():
    file = open("password_config.json")
    password_config = json.load(file)["password_requirements"]
    policy = PasswordPolicy.from_names(
        length=password_config["password_len"],  # min length: 10
        # need min. 1 uppercase letters
        uppercase=password_config["uppercase"],
        numbers=password_config["numbers"],  # need min. 1 digits
        # need min. 1 special characters
        special=password_config["special_char"],
        # need min. 1 non-letter characters (digits, specials, anything)
        nonletters=password_config["nonletters"]
    )
    return policy, password_config["salt_len"]

def get_config_rules_messages():
    file = open("password_config.json")
    return json.load(file)["rules_messages"]


def get_user_from_table(cursor, email):
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    return cursor.fetchone()