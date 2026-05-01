"""
Author: Alberth Matos
CYOP300
Date: 28 April 2026
Description: Helper functions for the user_admin page, handling user creation,
    removal, and password changes. Actual interaction with the database is
    handled by the db module, and validation of username (email address), name,
    and password are handled by the toolbox module.
"""

import db
from toolbox import is_valid_email, is_valid_name, validate_password


def create_user(name: str = "", username: str = "", password: str | None = None) -> str:
    """
    Creates a new user in the database.

    Validates input name and username and attempts to create a new user in the
    database. If the input is invalid or the user creation fails, an appropriate
    error message is returned. If the user is successfully created, a success
    message is returned.

    :param name: The full name of the user to be created.
    :type name: str
    :param username: The email address to be used as the username.
    :type username: str
    :param password: The password for the new user account. Defaults to None,
        which will generate an error message.
    :type password: str | None
    :return: A message indicating the result of the user creation process, either
        success or a specific error.
    :rtype: str
    """
    # Strip whitespace from both name and username to prevent malicious input.
    name = name.strip()
    username = username.strip()
    if not name or not name.strip():
        # Check to make sure name is not empty or only whitespace
        message = "Name is required when creating a user."
    elif not is_valid_name(name):
        # Check to make sure name is valid
        message = (
            "Invalid name format. Only alphabetic characters, spaces, "
            "hyphens, and apostrophes are allowed."
        )
    elif not username or not username.strip():
        # Check to make sure username is not empty or only whitespace
        message = "Username (e-mail address) is required when creating a user."
    elif not is_valid_email(username):
        # Check to make sure username is a valid email address-like string
        message = "Invalid email format. Please provide a valid email address."
    elif not password:
        # Check to make sure password is not empty
        message = "Password is required when creating a user."
    elif not validate_password(password):
        # Check to make sure password meets the requirements
        message = "Password does not meet requirements."
    else:
        # If all checks pass, proceed with user creation.
        # Note, we really just throw away the returned message in this instance,
        # but normally, it would be useful to log it to a file for later review.
        user_created, error_message = db.create_user(name, username, password)
        if user_created:
            message = f"User '{username}' created."
        else:
            message = f"Error: User '{username}' was not created: {error_message}"
    return message


def delete_user(username: str = "", session_username: str | None = None) -> str:
    """
    Deletes a user from the database.

    This function performs several checks to ensure the user deletion request
    is valid. It requires the username of the user to be deleted and the
    username of the session user attempting the deletion. If the checks pass,
    it attempts to delete the user from the database.
    """
    # Define default variables
    succeeded = False

    # Check if the user is logged in. If not, return an error message. If the
    # user IS logged in, strip any whitespace from the session username.
    if session_username is None:
        message = "You must be logged in to delete a user."
        return message
    else:
        session_username = session_username.strip()
    # Strip any whitespace from the username to be deleted.
    username = username.strip()
    # If username is empty or only whitespace, stop the activity to prevent
    # possible malicious input.
    if not username or not username.strip():
        message = "A username is required."
    elif username == session_username:
        # If the username to be deleted is the same as the logged-in user,
        # throw an error. You cannot delete yourself.
        # This is meant as a cheap security measure to prevent an admin from
        # removing all admins, other than the default "admin" user, which is
        # protected as well from deletion.
        message = "You cannot delete yourself."
    elif username.lower() == "admin":
        # The default admin cannot be deleted.
        message = "You cannot delete the main admin user."
    else:
        # If all checks pass, proceed with user deletion.
        # Note, we really just throw away the returned message in this instance,
        # but normally, it would be useful to log it to a file for later review.
        succeeded, message = db.delete_user(username)
    if succeeded:
        message = f"User '{username}' deleted."
    return message


def change_password(username: str = "", password: str | None = None) -> str:
    """
    Changes the password for a specified user in the database.

    This function validates the provided username and new password before
    attempting to update the user’s password. If the username or password is
    invalid, an appropriate error message is returned.

    The function also ensures the new password meets all necessary requirements.

    :param username: The username whose password needs to be updated. Must not
        be empty or consist of only whitespace.
    :type username: str
    :param password: The new password to set for the user. Must meet all required
        password policies defined by the system.
    :type password: str or None
    :return: A message describing the result of the password change operation,
        including success or specific error details.
    :rtype: str
    """
    # Define default variables and strip whitespace from username.
    username = username.strip()
    succeeded = False
    # If username is empty or only whitespace, stop the activity to prevent
    # possible malicious input.
    if not username or not username.strip():
        message = "A username is required."
    # If password is empty or only whitespace, stop the activity to prevent
    # possible malicious input. An empty password would fail validation anyway,
    # so this is really extraneous.
    elif not password or not password.strip():
        message = "A new password is required."
    else:
        # If the password does not pass validation, stop the activity.
        password_passes = validate_password(password)
        if not password_passes:
            message = "Password does not meet requirements."
        else:
            # If all checks pass, proceed with password change.
            # Note, we really just throw away the returned message in this instance,
            # but normally, it would be useful to log it to a file for later review.
            succeeded, message = db.change_password(username, password)
    if succeeded:
        message = f"Password changed for user '{username}'."
    return message
