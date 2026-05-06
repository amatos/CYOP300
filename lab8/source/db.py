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
    - Database connections are wrapped with `closing(...)` so they are always
      closed after use.
    - The sqlite connection context manager handles commits and rollbacks.
    - Any queries to the database should be parameterized to prevent SQL
      injection attacks.
"""

import sqlite3
from contextlib import closing
from pathlib import Path

import app_logging
from toolbox import hash_password, validate_password

logger = app_logging.get_logger(__name__)

# Module constant containing the path to the database file.
DATABASE_PATH = Path(__file__).with_name("accounts.db")

GET_USERS_QUERY = """
                  SELECT users.id, users.name, users.username, roles.role
                  FROM users
                           JOIN roles ON users.role_id = roles.id
                  ORDER BY users.name \
                  """
DELETE_USER_QUERY = "DELETE FROM users WHERE username = ?"
UPDATE_PASSWORD_QUERY = "UPDATE users SET password = ? WHERE username = ?"
REGULAR_USER_ROLE_ID = 2
INSERT_USER_SQL = """
                  INSERT INTO users (name, username, password, role_id)
                  VALUES (?, ?, ?, ?) \
                  """


def insert_user(name: str, username: str, password: str) -> None:
    """
    Inserts a new user into the database with a hashed password and a regular user
    role. This function does not return any value and performs the operation
    directly on the database.

    :param name: The full name of the user.
    :type name: str
    :param username: The username to be assigned to the user.
    :type username: str
    :param password: The plaintext password to be hashed and stored.
    :type password: str
    :return: None
    """
    hashed_password = hash_password(password)

    with closing(sqlite3.connect(DATABASE_PATH)) as conn:
        with conn:
            cursor = conn.cursor()
            cursor.execute(
                INSERT_USER_SQL,
                (name, username, hashed_password, REGULAR_USER_ROLE_ID),
            )


def execute_db_write(query: str, parameters: tuple = ()) -> int:
    """
    Executes a write and returns the number of affected rows.

    :param query: Parameterized SQL query to execute.
    :param parameters: Values to bind to the SQL query.
    :return: Number of affected rows.
    """
    with closing(sqlite3.connect(DATABASE_PATH)) as conn:
        with conn:
            cursor = conn.cursor()
            cursor.execute(query, parameters)
            return cursor.rowcount


def query_rowcount_result(
    rowcount: int,
    not_found_message: str,
    success_message: str,
    duplicate_message: str | None = None,
) -> tuple[bool, str]:
    """
    Converts a database row count into a standardized success tuple.

    :param rowcount: Number of rows affected by a database operation.
    :param not_found_message: Message returned when no rows were affected.
    :param success_message: Message returned when exactly one row was affected.
    :param duplicate_message: Message returned when more than one row was affected.
    :return: Operation success status and message.
    """
    if rowcount == 0:
        return False, not_found_message

    if rowcount == 1 or duplicate_message is None:
        return True, success_message

    return False, duplicate_message


def get_users() -> tuple[list[tuple], bool, str]:
    """
    Fetches a list of users with their details such as ID, name, username,
    and role. The function retrieves data by executing a SQL query that joins the
    `users` table with the `roles` table based on the role ID. It orders the
    result by the user's name in ascending order.

    :return: A list of tuples, where each tuple contains the user's ID, name,
        username, and role from the database. If there is an error during execution,
        an empty list is returned instead.
    :rtype: tuple[list[tuple], bool, str]
    """
    try:
        with closing(sqlite3.connect(DATABASE_PATH)) as conn:
            with conn:
                cursor = conn.cursor()
                cursor.execute(GET_USERS_QUERY)
                return cursor.fetchall(), True, ""
    except sqlite3.Error as e:
        return [], False, f"Database error while fetching users: {e}"


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
    # Normalize usernames to lower case, and strip whitespace.
    # email addresses are not case sensitive, so this helps prevent malicious
    # input.
    username = username.lower().strip()
    try:
        rowcount = execute_db_write(DELETE_USER_QUERY, (username,))
    except sqlite3.Error as e:
        logger.error("Error deleting user %s: %r", username, e, exc_info=True)
        return False, f"Error deleting user: {e}"
    logger.info("User %s deleted successfully.", username)
    return query_rowcount_result(
        rowcount,
        f"Could not delete user: {username} does not exist.",
        f"User {username} deleted successfully.",
    )


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
    password_is_valid = validate_password(password)

    if not password_is_valid:
        raise ValueError("Password does not meet complexity requirements.")

    try:
        rowcount = execute_db_write(
            UPDATE_PASSWORD_QUERY,
            (hash_password(password), username),
        )
    except sqlite3.Error as e:
        logger.error(r"Error updating user password: %s", e, exc_info=True)
        return False, f"Error updating user password: {e}."

    return query_rowcount_result(
        rowcount,
        f"Could not update user password: User {username} does not exist.",
        f"User {username} password updated successfully.",
        f"Error updating user password: Multiple users with username {username} found.",
    )


def authenticate_user(username: str, password: str) -> tuple[bool, str]:
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
    stored_hash = ""
    succeeded = False
    message = ""
    try:
        with closing(sqlite3.connect(DATABASE_PATH)) as conn:
            with conn:
                c = conn.cursor()
                c.execute("SELECT password FROM users WHERE username = ?", (username,))
                # Fetch the first row of the result set, which should contain the
                # hashed password
                stored_hash = c.fetchone()
    except sqlite3.Error as e:
        # If we get an error, we return False and the error message.
        succeeded = False
        message = f"Error password for login: {e}"
        logger.error("Error password for login: %s", e, exc_info=True)
    else:
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
        with closing(sqlite3.connect(DATABASE_PATH)) as conn:
            with conn:
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
    normalized_name = name.strip()
    normalized_username = username.lower().strip()

    if not validate_password(password):
        return False, ""

    try:
        insert_user(normalized_name, normalized_username, password)
    except sqlite3.IntegrityError:
        message = f"Username {normalized_username} already exists."
        logger.warning(
            "Attempted to create %s, but %s already exists.",
            normalized_username,
            normalized_username,
        )
        return False, message
    except sqlite3.Error as error:
        message = f"Error creating user: {error}"
        logger.error("Error creating user: %s", error)
        return False, message

    message = f"User {normalized_username} created successfully."
    logger.info("User %s created successfully.", normalized_username)
    return True, message
