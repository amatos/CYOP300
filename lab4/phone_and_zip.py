"""
Author: Alberth Matos
CYOP300
Date: 07 April 2026
Description:
"""

import re


def validate_value(value: str, pattern: str) -> bool:
    """
    This function checks if the provided string, value, conforms to
    the regex, pattern. It returns a boolean indicating the success or
    failure of the match operation.

    :param value: The input string to validate against the provided pattern.
    :type value: str
    :param pattern: The regular expression pattern the input string should match.
    :type pattern: str
    :return: True if the input string matches the pattern, otherwise False.
    :rtype: bool
    """
    # re.match() returns a match object if the pattern matches the entire
    # string, or None if it does not. Convert this to a boolean, which is then
    # returned to the calling function.
    pattern_matches = bool(re.match(pattern, value))
    return pattern_matches


def get_phone() -> str:
    """
    Retrieves a phone number input from the user, which is then validated
    against a regex using validate_value(). The phone number must follow the
    format XXX-XXX-XXXX. It repeatedly prompts the user until a valid input is
    provided.

    :return: A phone number string that adheres to the XXX-XXX-XXXX format
    :rtype: str
    """
    # Get user input, strip any whitespace.
    phone = input("Enter your phone number (XXX-XXX-XXXX): ").strip()
    # Validate the input against the regex pattern. If it does not match,
    # prompt the user to re-enter until a valid format is provided.
    while not validate_value(value=phone, pattern=r"^\d{3}-\d{3}-\d{4}$"):
        print("Your phone number is not in correct format. Please re-enter:")
        phone = input("Enter your phone number (XXX-XXX-XXXX): ").strip()
    return phone


def get_zipcode() -> str:
    """
    Gets a valid ZIP+4 code from user input. The function repeatedly prompts
    the user to enter their ZIP+4 code in the format XXXXX-XXXX, where X is a
    digit, until a valid value is provided.

    :return: A valid ZIP+4 code entered by the user.
    :rtype: str
    """
    # Get user input, strip any whitespace.
    zipcode = input("Enter your zip code in ZIP+4 format (XXXXX-XXXX): ").strip()
    # Validate the input against the regex pattern. If it does not match,
    # prompt the user to re-enter until a valid format is provided, with
    # instructions to use 0000 as the +4 component if it is not known.
    while not validate_value(value=zipcode, pattern=r"^\d{5}-\d{4}$"):
        print(
            "Your zip code is not in correct format. If you do not know your "
            "+4 code, please use 0000."
        )
        zipcode = input("Enter your zip code+4 (XXXXX-XXXX): ").strip()
    return zipcode
