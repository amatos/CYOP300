"""
Author: Alberth Matos
CYOP300
Date: 28 April 2026
Description: The main entry point for the Lab 7 program. Flask executes this
module via 'flask run' or 'python3 app.py'.

"""

import hashlib
import sqlite3
from pathlib import Path

DATABASE_PATH = Path(__file__).with_name("accounts.db")
PASSWD_MIN_LOWER = 1
PASSWD_MIN_UPPER = 1
PASSWD_MIN_DIGITS = 1
PASSWD_MIN_SPECIAL = 1
PASSWD_MIN_LENGTH = 12


def hash_password(password: str) -> str:
    """
    Hashes a given password using the SHA-256 hashing algorithm.

    This function takes a password as input, encodes it to bytes, and computes
    its SHA-256 hash. The resulting hash is returned as a hexadecimal string.

    :param password: The plain-text password to be hashed
    :type password: str
    :return: The hexadecimal representation of the hashed password
    :rtype: str
    """
    return hashlib.sha256(password.encode()).hexdigest()


def validate_password(password: str = "") -> bool:
    """
    Validate a password against defined security policies.

    This function enforces a set of password security rules defined by
    the PasswordPolicy module and additional custom checks. The password is
    deemed valid if it satisfies the requirements on length, uppercase
    letters, digits, special characters, and the minimum number of
    lowercase letters.

    :param password: The password string to be validated.
    :type password: str, optional
    :return: A boolean indicating whether the password meets all security
        requirements. Returns True if the password is valid, False otherwise.
    :rtype: bool
    """
    check_policy = []
    check_lowercase = 0
    policy = PasswordPolicy.from_names(
        length=PASSWD_MIN_LENGTH,  # minimum length
        uppercase=PASSWD_MIN_UPPER,  # minimum 1 uppercase letter
        numbers=PASSWD_MIN_DIGITS,  # minimum 1 digit
        special=PASSWD_MIN_SPECIAL,  # minimum 1 special character
    )
    check_policy = policy.test(password)
    if not check_policy:
        check_lowercase = PasswordStats(password).letters_lowercase
    if check_lowercase >= PASSWD_MIN_LOWER:
        return True
    return False


def get_users() -> tuple[list[tuple], bool, str]:
    """
    Fetches a list of users with their details such as ID, name, username, and role.

    The function retrieves data by executing a SQL query that joins the `users` table
    with the `roles` table based on the role ID. It orders the result by the user's
    name in ascending order. It ensures proper resource management by closing the
    database connection at the end of execution.

    :return: A list of tuples, where each tuple contains the user's ID, name,
        username, and role from the database. If there is an error during execution,
        an empty list is returned instead.
    :rtype: list[tuple]
    """
    users = []
    succeeded = False
    message = ""
    try:
        with sqlite3.connect(DATABASE_PATH) as conn:
            c = conn.cursor()
            c.execute("""
                      SELECT users.id, users.name, users.username, roles.role
                      FROM users
                               JOIN roles ON users.role_id = roles.id
                      ORDER BY users.name
                      """)
            users = c.fetchall()
            succeeded = True
    except sqlite3.Error as e:
        succeeded = False
        message = f"Error: {e}: Unable to connect to database."
    finally:
        conn.close()
    return users, succeeded, message


def delete_user(username: str) -> tuple[bool, str]:
    """
    Deletes a user from the database based on the provided username.

    This function attempts to remove a user identified by the specified username
    from the database. If the operation is successful, a success message is returned.
    If an error occurs during the process, a failure message is returned instead.

    :param username: The username of the user to be deleted.
    :type username: str
    :return: A tuple indicating whether the operation succeeded and an associated
        message. The first element is a boolean (True if succeeded, False otherwise),
        and the second element is a string containing the success or error message.
    :rtype: tuple[bool, str]
    """
    try:
        with sqlite3.connect(DATABASE_PATH) as conn:
            c = conn.cursor()
            c.execute("DELETE FROM users WHERE username = ?", (username,))
    except sqlite3.IntegrityError as e:
        succeeded = False
        message = f"Username {username} already exists: {e}"
    except sqlite3.Error as e:
        succeeded = False
        message = f"Error deleting user: {e}: User does not exist."
    else:
        if c.rowcount == 0:
            succeeded = False
            message = f"Could not delete user: {username} does not exist."
        else:
            succeeded = True
            message = f"User {username} deleted successfully."
    finally:
        conn.close()
    return succeeded, message


def change_password(username: str, password: str) -> tuple[bool, str]:
    """
    Changes the password of a specified user. Validates the new password and updates it
    in the database if the validation is successful. In case of issues, raises appropriate
    errors or returns a status message indicating success or failure of the operation.

    :param username: The username of the user whose password is being changed.
    :param password: The new password to be set for the user.
    :return: A tuple containing a boolean indicating success or failure and a status message.
    :rtype: tuple[bool, str]
    :raises ValueError: If the password does not pass validation criteria.
    """
    succeeded = False
    message = ""
    password_is_valid, error_message = validate_password(password)
    if not password_is_valid:
        raise ValueError(error_message)

    try:
        with sqlite3.connect(DATABASE_PATH) as conn:
            c = conn.cursor()
            c.execute(
                "UPDATE users SET password = ? WHERE username = ?",
                (hash_password(password), username),
            )
    except sqlite3.Error as e:
        succeeded = False
        message = f"Error updating user password: {e}."
    else:
        if c.rowcount == 0:
            succeeded = False
            message = f"Could not update user password: User {username} does not exist."
        elif c.rowcount == 1:
            succeeded = True
            message = f"User {username} password updated successfully."
        elif c.rowcount >= 1:
            succeeded = False
            message = f"Error updating user password: Multiple users with username {username} found."
    finally:
        conn.close()
    return succeeded, message


def authenticate_user(username: str, password: str) -> tuple[bool, str | None]:
    """
    Authenticates a user by verifying their username and password against stored
    credentials in the database. The function checks if the provided password matches
    the stored password for the supplied username.

    :param username: The username of the user to authenticate.
    :type username: str
    :param password: The password of the user to authenticate.
    :type password: str
    :return: A tuple where the first element is a boolean indicating whether the
        authentication succeeded, and the second element is an optional string with an
        error message if authentication failed.
    :rtype: tuple[bool, str | None]
    """

    stored_password = ""
    try:
        with sqlite3.connect(DATABASE_PATH) as conn:
            c = conn.cursor()
            c.execute("SELECT password FROM users WHERE username = ?", (username,))
            stored_password = c.fetchone()
    except sqlite3.IntegrityError as e:
        succeeded = False
        message = f"Username {username} already exists: {e}"
    except sqlite3.Error as e:
        succeeded = False
        message = f"Error deleting user: {e}: User does not exist."
    else:
        if stored_password:
            succeeded = True
            message = f"User {username} logged in successfully."
        else:
            succeeded = False
            message = f"User {username} does not exist."
    finally:
        conn.close()
    if succeeded and stored_password and hash_password(password) == stored_password[0]:
        return True, message
    return False, message


def user_is_admin(username: str) -> bool:
    """
    Determines if a user has an 'admin' role based on their username.

    The function checks the user's role in the database by joining tables `users` and
    `roles`. If a user's role is found and matches "admin", the function returns `True`.
    Otherwise, it returns `False`. Any encountered database errors are handled gracefully.

    :param username: The username of the user to check for admin privileges.
    :type username: str
    :return: A boolean indicating whether the user has an admin role.
    :rtype: bool
    """
    role = None
    try:
        with sqlite3.connect(DATABASE_PATH) as conn:
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
    except sqlite3.IntegrityError:
        succeeded = False
    except sqlite3.Error:
        succeeded = False
    else:
        succeeded = True
    finally:
        conn.close()
    if succeeded and role is not None and role[0].lower() == "admin":
        return True
    return False


def create_user(name: str, username: str, password: str) -> tuple[bool, str]:
    """
    Validates the provided password, checks for username uniqueness in the database,
    and creates a new user in the database with the specified details. The function
    returns a status indicating if the user creation was successful and an error
    message if applicable.

    :param name: The name of the user.
    :type name: str
    :param username: The desired username for the user.
    :type username: str
    :param password: The password for the user.
    :type password: str
    :return: A tuple where the first element indicates if the operation was
        successful (True or False) and the second element provides an error
        message if the operation failed or an empty string if successful.
    :rtype: tuple[bool, str]
    """

    password_is_valid, error_message = validate_password(password)
    if not password_is_valid:
        return False, error_message

    try:
        with sqlite3.connect(DATABASE_PATH) as conn:
            c = conn.cursor()
            hashed_password = hash_password(password)
            c.execute(
                "INSERT INTO users (name, username, password, role_id) VALUES (?, ?, ?, ?)",
                (name, username, hashed_password, 2),
            )
    except sqlite3.IntegrityError:
        succeeded = False
        message = f"Username {username} already exists."
    except sqlite3.Error as e:
        succeeded = False
        message = f"Error creating user: {e}: Unable to connect to database."
    else:
        succeeded = True
        message = f"User {username} created successfully."
    finally:
        conn.close()
    return succeeded, message
