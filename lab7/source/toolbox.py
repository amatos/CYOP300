"""
Author: Alberth Matos
CYOP300
Date: 28 April 2026
Description: Helper functions for validating user input, such as names, email
addresses, and passwords, as well as hashing passwords.

"""

import hashlib
import re
from password_strength import PasswordPolicy, PasswordStats

# Define the password policy constants.
PASSWD_MIN_LOWER = 1
PASSWD_MIN_UPPER = 1
PASSWD_MIN_DIGITS = 1
PASSWD_MIN_SPECIAL = 1
PASSWD_MIN_LENGTH = 12


def is_valid_name(name: str) -> bool:
    """
    Check whether a given name meets specific formatting requirements.

    Validate that the provided name only consists of Aa-Zz, spaces, commas,
    apostrophes and dashes. In the real world, this might be too restrictive,
    as it would limit user names to roman letters that fit in the ascii
    character set, and would exclude any names with ordinals or diacritics
    as defined in ISO-8859-1, -2, -4, -7, -16, or any other character set.
    The functional purpose is to prevent a Little Bobby Tables* incident.
    *see https://xkcd.com/327/

    :param name: The input string representing the name to be validated.

    :return: A boolean indicating whether the provided name adheres to the
        specified format.
    """

    name_pattern = r"^[A-Za-z]+(?:[ ,'-][A-Za-z]+)*$"
    return bool(re.fullmatch(name_pattern, name))


def is_valid_email(email: str) -> bool:
    """
    Check if the provided email address is in a valid format.

    Validate that the provided email address is in the correct format,
    without attempting to validate that the email address is actually valid
    or correct.
    The functional purpose is to prevent a Little Bobby Tables* incident.

    :param email: The email address to validate.
    :type email: str
    :return: True if the email address matches the expected format, False otherwise.
    :rtype: bool
    """

    email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.fullmatch(email_pattern, email))


def validate_password(password: str = "") -> bool:
    """
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
    # Define initial values
    check_policy = []
    check_lowercase = 0
    # Define the password policy, using constants defined in the module header
    policy = PasswordPolicy.from_names(
        length=PASSWD_MIN_LENGTH,  # minimum length
        uppercase=PASSWD_MIN_UPPER,  # minimum 1 uppercase letter
        numbers=PASSWD_MIN_DIGITS,  # minimum 1 digit
        special=PASSWD_MIN_SPECIAL,  # minimum 1 special character
    )
    # Test the password against the policy. A successful check will return an
    # empty list.
    check_policy = policy.test(password)
    if not check_policy:
        # If we received an empty list, then the check suceeded.
        # We now check for a minimum number of lowercase characters, as
        # PasswordPolicy only checks the number of uppercase letters, and we
        # explicitly want lower case as well.
        check_lowercase = PasswordStats(password).letters_lowercase
        if check_lowercase >= PASSWD_MIN_LOWER:
            # If the minimum number of lower case letters is also met, return
            # True, as this password passws all of our checks.
            return True
    return False


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
