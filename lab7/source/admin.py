"""
Author: Alberth Matos
CYOP300
Date: 28 April 2026
Description: The main entry point for the Lab 7 program. Flask executes this
module via 'flask run' or 'python3 app.py'.

"""

import db


def create_user(name: str = "", username: str = "", password: str | None = None) -> str:
    """
    Creates a new user in the system with the provided name, username, and
    password. If any of the required parameters are missing or invalid, an
    appropriate error message is returned. This function handles exceptions
    that might occur during the creation process and ensures a user-friendly
    response.

    :param name: The full name of the user to be created. This is a required
        parameter.
    :type name: str
    :param username: The email address of the user to be created. This acts as
        the unique identifier for the user. It is required.
    :type username: str
    :param password: The password for the user to be created. This is required,
    unless explicitly set to None.
    :type password: str | None
    :return: A status message indicating the success or failure of the user
    creation process. If the user creation fails, the reason for the failure
    will be included in the message.
    :rtype: str
    """
    if name is None:
        message = "Name is required when creating a user."
    elif username is None:
        message = "Username (e-mail address) is required when creating a user."
    elif not password:
        message = "Password is required when creating a user."
    else:
        user_created, error_message = db.create_user(name, username, password)
        if user_created:
            message = f"User '{username}' created."
        else:
            message = f"Error: User '{username}' was not created: {error_message}"
    return message


def delete_user(username: str = "", session_username: str | None = None) -> str:
    """
    Deletes a user from the system based on the given username.

    This function performs several checks to ensure the user deletion request
    is valid. It requires the username of the user to be deleted and the
    username of the session user attempting the deletion. If the checks pass,
    it attempts to delete the user from the database.

    :param username: The username of the user to be deleted. Should be
        provided as a non-empty string.
    :param session_username: The username of the session user performing
        the deletion. If not provided, the operation assumes the user is
        not authenticated.
    :return: A string message indicating the result of the delete operation,
        including error messages if the operation could not be completed.
    """
    succeeded = False
    if username == "":
        message = "A username is required."
    elif session_username is None:
        message = "You must be logged in to delete a user."
    elif username == session_username:
        message = "You cannot delete yourself."
    elif username == "admin":
        message = "You cannot delete the main admin user."
    else:
        succeeded, message = db.delete_user(username)
    if succeeded:
        message = f"User '{username}' deleted."
    return message


def change_password(username: str = "", password: str | None = None) -> str:
    """
    Change the password for a given username, validating the new password against
    specific requirements.

    This function validates the provided username and password, ensuring the
    password meets specific conditions before proceeding to update the user's
    password in the database. Errors arising from validation or the update
    operation are caught and handled to provide a user-friendly message.

    :param username: The username for which the password needs to be changed.
    :type username: str
    :param password: The new password to be set. If None, it indicates that no new
        password was provided.
    :type password: str | None
    :return: A message indicating the result of the operation. Possible values:
        - "A username is required." if the username is an empty string.
        - "A new password is required." if the password is None.
        - "Password does not meet requirements." if the password fails
          validation checks.
        - "Password changed for user '<username>'." if the operation succeeds.
        - An error message if a `ValueError` is raised during execution.
        - "Unable to change password." for any unspecified exception.
    :rtype: str
    """
    succeeded = False
    if username == "":
        message = "A username is required."
    elif password is None:
        message = "A new password is required."
    else:
        password_passes = db.validate_password(password)
        if not password_passes:
            message = "Password does not meet requirements."
        succeeded, message = db.change_password(username, password)
    if succeeded:
        message = f"Password changed for user '{username}'."
    return message
