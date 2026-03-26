"""
Author: Alberth Matos
CYOP300
Date: 24 March 2026
Description: Provides a menu-driven terminal interface for my Lab2 application.
  The Prompt class contains two static methods: menu() and dict_menu().

  The menu() method takes a list of options and displays them in a terminal
  menu, allowing the user to select one.
  The dict_menu() method takes a dictionary of options, displays the keys as
  a menu, and executes the corresponding function based on the user's selection.
"""

import string
import random
import secrets

try:
    import lab2common
except ImportError:  # pragma: no cover
    from . import lab2common


def build_password_requirements() -> tuple[int, dict[str, int], str]:
    """Collect password requirements and return the target length, counts, and
    allowed characters."""
    print("Generate a secure password.\n")

    # Get the length of the desired password.
    password_length = lab2common.get_input(
        int, "Please enter the length of the password (Integers only): "
    )
    print("Please enter the complexity of the password via the following prompts:")

    # list containing the categories of characters to include in the password,
    # the prompt to present to the user, and the type of characters to include
    # in the password.
    categories = [
        ("upper", "Include uppercase letters? (y/n): ", string.ascii_uppercase),
        ("lower", "Include lowercase letters? (y/n): ", string.ascii_lowercase),
        ("digits", "Include digits? (y/n): ", string.digits),
        ("special", "Include special characters? (y/n): ", string.punctuation),
    ]

    # Initialize the required counts for each category to 0.
    required_counts = {name: 0 for name, _, _ in categories}
    allowed_characters = ""  # Initialize an empty string to store allowed characters

    # Loop through the categories, prompt the user for each category, and
    # initialize the required count to 1 for each category for which the user
    # selected `y'.
    for name, prompt, characters in categories:
        if lab2common.get_yes_no_input(prompt) == "y":
            required_counts[name] = 1
            # For each category that the user selected, append the characters
            # in each set to allowed_characters.
            allowed_characters += characters

    # If the password length is less than the sum of the required counts,
    # raise a ValueError.
    if password_length < sum(required_counts.values()):
        raise ValueError("Password length is too short for the selected complexity.")

    # Return the target length, required counts, and allowed characters.
    return password_length, required_counts, allowed_characters


def count_character_types(password: str) -> dict[str, int]:
    """Count the number of each character type in a password."""

    # Initialize a dictionary to store the counts of each character type.
    counts = {"upper": 0, "lower": 0, "digits": 0, "special": 0}
    # Parse through each character in the password, and increment the
    # corresponding count in the counts dictionary.
    for char in password:
        if char.isupper():
            counts["upper"] += 1
        elif char.islower():
            counts["lower"] += 1
        elif char.isdigit():
            counts["digits"] += 1
        elif char in string.punctuation:
            counts["special"] += 1
    return counts


def generate_password(
    password_length: int, required_counts: dict[str, int], allowed_characters: str
) -> str:
    """Generate a password that satisfies the required character counts."""
    password_chars = []

    for character_type, count in required_counts.items():
        if count > 0:
            if character_type == "upper":
                pool = string.ascii_uppercase
            elif character_type == "lower":
                pool = string.ascii_lowercase
            elif character_type == "digits":
                pool = string.digits
            else:
                pool = string.punctuation

            password_chars.extend(secrets.choice(pool) for _ in range(count))

    remaining_length = password_length - len(password_chars)
    password_chars.extend(
        secrets.choice(allowed_characters) for _ in range(remaining_length)
    )
    # Shuffle the password characters to randomize the order
    random.shuffle(password_chars)

    # Return the generated password as a string
    return "".join(password_chars)
