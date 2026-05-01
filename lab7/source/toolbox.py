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

# Validation patterns.
NAME_PATTERN = re.compile(r"^[A-Za-z]+(?:[ ,'-][A-Za-z]+)*$")
EMAIL_PATTERN = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")

# Password policy constants.
PASSWORD_MIN_LOWERCASE = 1
PASSWORD_MIN_UPPERCASE = 1
PASSWORD_MIN_DIGITS = 1
PASSWORD_MIN_SPECIAL = 1
PASSWORD_MIN_LENGTH = 12

# Password hashing constants.
PASSWORD_ENCODING = "utf-8"
PASSWORD_HASH_ALGORITHM = "sha256"


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
    return bool(NAME_PATTERN.fullmatch(name))


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
    return bool(EMAIL_PATTERN.fullmatch(email))


def build_password_policy() -> PasswordPolicy:
    """
    Build the password policy used by password validation.

    :return: Configured password policy.
    :rtype: PasswordPolicy
    """
    return PasswordPolicy.from_names(
        length=PASSWORD_MIN_LENGTH,
        uppercase=PASSWORD_MIN_UPPERCASE,
        numbers=PASSWORD_MIN_DIGITS,
        special=PASSWORD_MIN_SPECIAL,
    )


def validate_password(password: str = "") -> bool:
    """
    Validate whether a password satisfies the configured security rules.

    The password must satisfy the PasswordPolicy requirements for length,
    uppercase letters, digits, and special characters. It must also contain
    the configured minimum number of lowercase letters.

    :param password: The password string to be validated.
    :type password: str, optional
    :return: True if the password is valid, False otherwise.
    :rtype: bool
    """
    policy = build_password_policy()
    policy_violations = policy.test(password)

    if policy_violations:
        return False

    lowercase_count = PasswordStats(password).letters_lowercase
    if lowercase_count < PASSWORD_MIN_LOWERCASE:
        return False
    else:
        return True


def hash_password(password: str) -> str:
    """
    Hashes a given password using the configured hashing algorithm.

    This function takes a password as input, encodes it to bytes, and computes
    its hash. The resulting hash is returned as a hexadecimal string.

    :param password: The plain-text password to be hashed
    :type password: str
    :return: The hexadecimal representation of the hashed password
    :rtype: str
    """
    # encode password to bytes prior to feeding it into hashlib.hexdigest
    encoded_password = password.encode(PASSWORD_ENCODING)
    return hashlib.new(PASSWORD_HASH_ALGORITHM, encoded_password).hexdigest()
