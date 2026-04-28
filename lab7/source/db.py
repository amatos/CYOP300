import hashlib
import sqlite3
import string
from pathlib import Path

DATABASE_PATH = Path(__file__).with_name("accounts.sqlite")


def initialize_db_connection():
    return sqlite3.connect(DATABASE_PATH)


def close_db_connection(conn):
    conn.close()


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def validate_password(password):
    """
    Validates that a password meets the minimum security requirements.

    Password requirements:
    - At least 12 characters
    - At least 1 uppercase letter
    - At least 1 lowercase letter
    - At least 1 number
    - At least 1 symbol

    :param password: Password to validate.
    :type password: str
    :return: Tuple containing whether the password is valid and an error message.
    :rtype: tuple[bool, str]
    """
    if len(password) < 12:
        return False, "Password must be at least 12 characters long."

    if not any(character.isupper() for character in password):
        return False, "Password must contain at least one uppercase letter."

    if not any(character.islower() for character in password):
        return False, "Password must contain at least one lowercase letter."

    if not any(character.isdigit() for character in password):
        return False, "Password must contain at least one number."

    if not any(character in string.punctuation for character in password):
        return False, "Password must contain at least one symbol."

    return True, ""


def get_users():
    conn = initialize_db_connection()
    try:
        c = conn.cursor()
        c.execute("""
            SELECT users.id, users.name, users.username, roles.role
            FROM users
            JOIN roles ON users.role_id = roles.id
            ORDER BY users.name
            """)
        return c.fetchall()
    except sqlite3.Error as e:
        print(f"Error fetching users: {e}")
        return []
    finally:
        close_db_connection(conn)


def delete_user(username):
    conn = initialize_db_connection()
    try:
        c = conn.cursor()
        c.execute("SELECT username FROM users WHERE username = ?", (username,))

        if c.fetchone() is None:
            raise ValueError(f"Username {username} does not exist.")

        c.execute("DELETE FROM users WHERE username = ?", (username,))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error deleting user: {e}")
    finally:
        close_db_connection(conn)


def change_password(username, password):
    password_is_valid, error_message = validate_password(password)

    if not password_is_valid:
        raise ValueError(error_message)

    conn = initialize_db_connection()
    try:
        c = conn.cursor()
        c.execute(
            "UPDATE users SET password = ? WHERE username = ?",
            (hash_password(password), username),
        )
        conn.commit()
    finally:
        close_db_connection(conn)


def authenticate_user(username, password):
    conn = initialize_db_connection()
    try:
        c = conn.cursor()
        c.execute("SELECT password FROM users WHERE username = ?", (username,))
        stored_password = c.fetchone()

        if stored_password and hash_password(password) == stored_password[0]:
            return True
        return False
    except sqlite3.Error as e:
        print(f"Error authenticating user: {e}")
        return False
    finally:
        close_db_connection(conn)


def user_is_admin(username):
    conn = initialize_db_connection()
    try:
        c = conn.cursor()
        c.execute(
            """
            SELECT roles.role
            FROM users
            JOIN roles ON users.role_id = roles.id
            WHERE users.username = ?
            """,
            (username,),
        )
        role = c.fetchone()
        return role is not None and role[0].lower() == "admin"
    except sqlite3.Error as e:
        print(f"Error checking admin role: {e}")
        return False
    finally:
        close_db_connection(conn)


def create_user(name, username, password):
    password_is_valid, error_message = validate_password(password)

    if not password_is_valid:
        return False, error_message

    conn = initialize_db_connection()
    c = conn.cursor()
    username_exists = c.execute(
        "SELECT username FROM users WHERE username = ?", (username,)
    )
    if username_exists.fetchone():
        close_db_connection(conn)
        return False, f"Username {username} already exists."

    hashed_password = hash_password(password)
    c.execute(
        "INSERT INTO users (name, username, password, role_id) VALUES (?, ?, ?, ?)",
        (name, username, hashed_password, 2),
    )
    conn.commit()
    close_db_connection(conn)
    return True, ""
