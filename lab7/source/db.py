"""
Author: Alberth Matos
CYOP300
Date: 28 April 2026
Description: Helper module containing utility functions to interact with the
database. This module relies on sqlite3 for the database operations and Path
from pathlib for handling file paths. It also imports the validate_password
and hash_password function from the toolbox module to ensure password strength
before storing user credentials and to generate a hash of the password.

Note on database interactions:
    - `try`/`except`/`finally` block to connect to the database.
      The `with` block inside of the `try` block manages only commits and
      rollbacks, so we must explicitly handle closing the db connection
      in the `finally` block. Expected exceptions are handled within the
      `except` block.
    - Any queries to the database should be parameterized to prevent SQL
      injection attacks.
"""

import sqlite3
from pathlib import Path

from toolbox import validate_password, hash_password

# Module constant containing the path to the database file.
DATABASE_PATH = Path(__file__).with_name("accounts.db")


def get_users() -> tuple[list[tuple], bool, str]:
    """
    Fetches a list of users with their details such as ID, name, username,
    and role.

    The function retrieves data by executing a SQL query that joins the
    `users` table with the `roles` table based on the role ID. It orders the
    result by the user's name in ascending order.

    :return: A list of tuples, where each tuple contains the user's ID, name,
        username, and role from the database. If there is an error during execution,
        an empty list is returned instead.
    :rtype: list[tuple]
    """
    # Define initial values
    users = []
    succeeded = False
    message = ""
    # Please see the note in the docstring for more details on the
    # try/except/finally block
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
    # Please see the note in the docstring for more details on the
    # try/except/finally block
    try:
        with sqlite3.connect(DATABASE_PATH) as conn:
            c = conn.cursor()
            c.execute("DELETE FROM users WHERE username = ?", (username,))
    except sqlite3.Error as e:
        # If we get an error, we return False and the error message.
        succeeded = False
        message = f"Error deleting user: {e}"
    else:
        # Otherwise, we need to parse the response from the database. If
        # there were no rows affected, then we know the user did not exist.
        # If one or more rows were affected, then we know that the user was
        # deleted. The result never should be >1, as the username is supposed
        # to be unique, based on create_user and on a database constraint.
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
    Changes the password of a specified user.

    Validates the new password and updates it in the database if the validation
    is successful. In case of issues, raises appropriate errors or returns a
    status message indicating success or failure of the operation.

    :param username: The username of the user whose password is being changed.
    :param password: The new password to be set for the user.
    :return: A tuple containing a boolean indicating success or failure and a status message.
    :rtype: tuple[bool, str]
    :raises ValueError: If the password does not pass validation criteria.
    """
    # Define initial values
    succeeded = False
    message = ""
    # Validate the password
    password_is_valid, error_message = validate_password(password)
    # If the password does not pass validation, stop the activity.
    if not password_is_valid:
        raise ValueError(error_message)
    # Please see the note in the docstring for more details on the
    # try/except/finally block
    try:
        with sqlite3.connect(DATABASE_PATH) as conn:
            c = conn.cursor()
            c.execute(
                "UPDATE users SET password = ? WHERE username = ?",
                (hash_password(password), username),
            )
    except sqlite3.Error as e:
        # If we get an error, we return False and the error message.
        succeeded = False
        message = f"Error updating user password: {e}."
    else:
        # Otherwise, we need to parse the response from the database. If
        # there were no rows affected, then we know the user did not exist, so
        # we could not change the password. If one row was affected, then we
        # know that the user's password was changed. The result never should
        # be >1, as the username is supposed to be unique, based on
        # create_user, and on a database constraint, so we return an error,
        # HOWEVER, since this should never happen, we still have changed the
        # password, so technically, this is a security issue.
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
    credentials in the database. The function checks if the provided password's
    hash matches the stored password hash for the supplied username. We never
    store the actual plain-text password.

    :param username: The username of the user to authenticate.
    :type username: str
    :param password: The password of the user to authenticate.
    :type password: str
    :return: A tuple where the first element is a boolean indicating whether the
        authentication succeeded, and the second element is an optional string
        with an error message if authentication failed.
    :rtype: tuple[bool, str | None]
    """
    # Define initial values
    stored_hash = ""
    succeeded = False
    message = ""
    # Please see the note in the docstring for more details on the
    # try/except/finally block
    try:
        with sqlite3.connect(DATABASE_PATH) as conn:
            c = conn.cursor()
            c.execute("SELECT password FROM users WHERE username = ?", (username,))
            # Fetch the first row of the result set, which should contain the
            # hashed password
            stored_hash = c.fetchone()
    except sqlite3.Error as e:
        # If we get an error, we return False and the error message.
        succeeded = False
        message = f"Error password for login: {e}"
    else:
        #
        if stored_hash and hash_password(password) == stored_hash[0]:
            # If the stored hash matches the provided password, we return True.
            succeeded = True
            message = f"User {username} logged in successfully."
        else:
            # Otherwise, we return False and an error message. Note that the
            # error message is not specific whether the problem was with the
            # username or the password. This is to prevent attempts at
            # brute-forcing passwords once one knows that the username
            # itself exists.
            succeeded = False
            message = f"User {username} unable to log in."
    finally:
        conn.close()
    return succeeded, message


def user_is_admin(username: str) -> bool:
    """
    Determines if a user has an 'admin' role based in the database.

    The function checks the user's role in the database by joining tables `users` and
    `roles`. If a user's role is found and matches "admin", the function returns `True`.
    Otherwise, it returns `False`. Any encountered database errors are handled gracefully.

    :param username: The username of the user to check for admin privileges.
    :type username: str
    :return: A boolean indicating whether the user has an admin role.
    :rtype: bool
    """
    # Define initial values
    role = None
    succeeded = False
    # Please see the note in the docstring for more details on the
    # try/except/finally block
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
    except sqlite3.Error:
        # If we get an error, we return False and the error message.
        succeeded = False
    else:
        if role is not None and role[0].lower() == "admin":
            # `role` should only ever be "admin" or "user". Since we only
            # care if the user is an admin, we can just check if there IS a
            # role defined (which should always be the case), and if that role
            # is "admin".
            succeeded = True
    finally:
        conn.close()
    return succeeded


def create_user(name: str, username: str, password: str) -> tuple[bool, str]:
    """
    Creates a user in the database as a regular `user`.

    Validates the provided password, checks for username uniqueness in the
    database, and creates a new user in the database with the specified
    details, with the role hardcoded as `user`. The function returns a status
    indicating if the user creation was successful and an error message if
    applicable.

    Note that at this time, there is NO functionality to create an admin user,
    or to change a user's role.

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
    # Define initial values
    succeeded = False
    message = ""
    # Validate the password
    password_is_valid, message = validate_password(password)
    # If the password does not pass validation, stop the activity.
    if not password_is_valid:
        return succeeded, message
    # Please see the note in the docstring for more details on the
    # try/except/finally block
    try:
        with sqlite3.connect(DATABASE_PATH) as conn:
            c = conn.cursor()
            hashed_password = hash_password(password)
            c.execute(
                "INSERT INTO users (name, username, password, role_id) VALUES (?, ?, ?, ?)",
                (name, username, hashed_password, 2),
            )
    except sqlite3.IntegrityError:
        # An integrity error indicates that the username is already in use.
        # The database enforces uniqueness on users.username via a constraint.
        succeeded = False
        message = f"Username {username} already exists."
    except sqlite3.Error as e:
        # If we get an error, we return False and the error message.
        succeeded = False
        message = f"Error creating user: {e}"
    else:
        succeeded = True
        message = f"User {username} created successfully."
    finally:
        conn.close()
    return succeeded, message
