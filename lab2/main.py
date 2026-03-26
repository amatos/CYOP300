"""
Author: Alberth Matos
CYOP300
Date: 24 March 2026
Description: Produce a command line menu-driven python application providing
users with the ability to perform some math and security-related functions:
    A. Generate Secure Password.
    B. Calculate and Format a Percentage.
    C. How many days from today until July 4, 2025?
    D. Use the Law of Cosines to calculate the leg of a triangle.
    E. Calculate the volume of a Right Circular Cylinder.
    F. Exit program.
"""

import sys
import datetime
import math

try:
    import lab2passwd
    import lab2common
    import lab2prompt
except ImportError:  # pragma: no cover
    from . import lab2passwd
    from . import lab2common
    from . import lab2prompt


def generate_secure_password() -> None:
    """
    Generates a secure password based on user input for length and complexity.

    :return: None
    :rtype: None
    """
    proceed = True  # Flag to control the try-except block
    password_length = 0  # Integer to store the password length
    required_counts = {}  # Dictionary to store the required character counts
    allowed_characters = ""  # String to store the allowed characters for the password

    # Since lab2passwd.build_password_requirements() can raise a ValueError
    # exception, we need to catch any exceptions and handle them gracefully. In
    # this case, we wrap up the call to lab2passwd.build_password_requirements()
    # in a try-except block, and if there is a ValueError exception, we print
    # an error message asking the user to re-enter their input and set proceed
    # to False.

    try:
        password_length, required_counts, allowed_characters = (
            lab2passwd.build_password_requirements()
        )
    except ValueError as e:
        # n.b.: we only print a message and set a flag, not re-prompt the user.
        print(f"\nInvalid input: {e}\n\nPlease try again.\n")
        proceed = False

    if proceed:
        # If proceed is True, we can safely generate the password.
        password = lab2passwd.generate_password(
            password_length, required_counts, allowed_characters
        )
        print(f"Your secure password is: {password}")

        # While not in the lab requirements, as a useful sanity check, we
        # count the number of each character type in the password and print
        # the results.
        password_count = lab2passwd.count_character_types(password)
        print("\nYour password consists of:")
        for category, count in password_count.items():
            print(f"{count} {category} characters")

    # If either proceed is false, or, if the section immediately above, where
    # proceed is true, executes, we then prompt the user for what they would
    # like to do next, again using the dict_menu() function from the prompt module.
    options = {
        "Generate a new Secure Password": generate_secure_password,
        "Return to Main Menu": main,
        "Exit": exit_program,
    }
    lab2prompt.Prompt.dict_menu(options)


def calculate_percentage() -> None:
    """Calculates the percentage of a given number, based on user-provided
    numerator, denominator, and decimal places.

    :return: None
    :rtype: None
    """

    # Print the instructions for the user.
    print("Enter the numerator, denominator, and decimal places:")
    # Use lab2common.get_input() to get the user's input.
    # For numerator and denominator, we get the input as floats to handle
    # decimal places.
    # For decimal places, we get the input as an integer, since it represents
    # the number of decimal places to display, which requires a whole number.
    numerator = lab2common.get_input(float, "Numerator: ")
    denominator = lab2common.get_input(float, "Denominator: ")
    decimal_places = lab2common.get_input(int, "Decimal Places: ")

    if denominator == 0:
        # Protect from a division by zero error by checking if the denominator
        # is zero before performing the calculation. If the denominator is
        # zero, we print an error message and prompt the user for what they
        # would like to do next, again using the dict_menu() function from
        # the prompt module.
        print("Error: Denominator cannot be zero.")
        options = {
            "Calculate and Format a Percentage": calculate_percentage,
            "Return to Main Menu": main,
            "Exit": exit_program,
        }
        lab2prompt.Prompt.dict_menu(options)

    if decimal_places < 0:
        # Protect from a ValueError by checking if the decimal place is less
        # than zero before performing the calculation. If the decimal place is
        # less than zero, we print an error message and prompt the user for what
        # they would like to do next, again using the dict_menu() function from
        # the prompt module.
        print("Error: Decimal places cannot be negative.")
        options = {
            "Calculate and Format a Percentage": calculate_percentage,
            "Return to Main Menu": main,
            "Exit": exit_program,
        }
        lab2prompt.Prompt.dict_menu(options)
    # For the percentage, we calculate it by dividing the numerator by the
    # denominator, and then multiply the result by 100.
    percentage = (numerator / denominator) * 100
    # The percentage is then formatted with the user-specified decimal places.
    print(f"{numerator}/{denominator} = {percentage:.{decimal_places}f} %")

    # Prompt the user for what they would like to do next, again using the
    # dict_menu() function from the prompt module.
    options = {
        "Calculate and Format a Percentage": calculate_percentage,
        "Return to Main Menu": main,
        "Exit": exit_program,
    }
    lab2prompt.Prompt.dict_menu(options)


def calculate_days_until_july_4() -> None:
    """Calculates the number of days between today and July 4, 2025.

    :return: None
    :rtype: None
    """

    # Target date is July 4, 2025.
    target_date = datetime.date(2025, 7, 4)
    current_date = datetime.date.today()  # Today's date
    # Difference, in days, between the two dates.
    days_delta = (target_date - current_date).days
    # Print the results.
    # Note, the code is written so that if the target date is in the past,
    # the message will indicate that the target date (July 4th 2025) has
    # already passed, and will be in the past tense.  The number of days
    # will be multiplied by -1 to give a positive value.
    # If the target date had been in the future, the else statement would
    # print, indicating a positive number of days until the target date.
    if days_delta < 0:
        print(f"July 4, 2025 occurred {days_delta * -1} days ago.")
    else:
        print(f"There are {days_delta} days until July 4, 2025.")
    # Prompt the user for what they would like to do next, again using the
    # dict_menu() function from the prompt module.
    options = {
        "How many days from today until July 4, 2025?": calculate_days_until_july_4,
        "Return to Main Menu": main,
        "Exit": exit_program,
    }
    lab2prompt.Prompt.dict_menu(options)


def calculate_triangle_leg() -> None:
    """Calculates the leg of a triangle based on user-provided side lengths.
    using the Law of Cosines.  The Law of Cosines is:
        c^2 = a^2 + b^2 − (2ab cos(C))
    or:
        c = sqrt(a^2 + b^2 − (2ab cos(C)))

    :return: None
    :rtype: None
    """
    print("Enter the lengths of the sides of the triangle:")
    length_a = lab2common.get_input(float, "Side a: ")
    length_b = lab2common.get_input(float, "Side b: ")
    angle_c = lab2common.get_input(float, "Angle C (in degrees): ")
    # Convert angle C from degrees to radians, since the math.cos() function
    # expects the angle to be in radians.
    angle_c_in_rad = math.radians(angle_c)
    # Calculate the leg of the triangle using the Law of Cosines.
    leg_c = math.sqrt(
        length_a**2 + length_b**2 - (2 * length_a * length_b * math.cos(angle_c_in_rad))
    )
    # Print the result.
    # N.b., the lab requirements do not specify the number of decimal places
    # to display, so I have chosen to display 2 decimal places.
    print(f"The length of the leg of the triangle is: {leg_c:.2f}")

    # Prompt the user for what they would like to do next, again using the
    # dict_menu() function from the prompt module.
    options = {
        "Use the Law of Cosines to calculate the leg of a triangle.": (
            calculate_triangle_leg
        ),
        "Return to Main Menu": main,
        "Exit": exit_program,
    }
    lab2prompt.Prompt.dict_menu(options)


def calculate_cylinder_volume() -> None:
    """Calculates the volume of a right circular cylinder based on user-provided
    radius and height. Outout units are in mm^3.

    Formula: V = πr^2h
    (Volume = π * radius^2 * height)

    :return: None
    :rtype: None
    """

    print("Enter the radius and height of the cylinder:")
    radius, radius_unit = lab2common.get_input_in_mm("radius", "radius of the circle")
    height, height_unit = lab2common.get_input_in_mm("height", "height of the cylinder")

    volume = math.pi * radius**2 * height
    volume_unit = "mm^3"

    # Print the result.
    print(f"The volume of the cylinder is: {volume:.2f} {volume_unit}")
    # Prompt the user for what they would like to do next, again using the
    # dict_menu() function from the prompt module.
    options = {
        "Calculate the volume of a Right Circular Cylinder": calculate_cylinder_volume,
        "Return to Main Menu": main,
        "Exit": exit_program,
    }
    lab2prompt.Prompt.dict_menu(options)


def exit_program() -> None:
    """Exits the program.

    :return: None
    :rtype: None
    """
    print("Exiting program. Thank you for using me!")
    sys.exit(0)


def main():
    """
    This is the main function that serves as the entry point for the program.
    It provides a menu-driven interface using TerminalMenu (see lab2prompt.py
    for implementation), which allows users to select from a set of tasks
    as required by the Lab documentation.

    :return: None
    :rtype: None
    """

    # Define the menu options and their corresponding functions in a dictionary.
    options = {
        "a. Generate Secure Password": generate_secure_password,
        "b. Calculate and Format a Percentage": calculate_percentage,
        "c. How many days from today until July 4, 2025?": calculate_days_until_july_4,
        "d. Use the Law of Cosines to calculate the leg of a triangle.": (
            calculate_triangle_leg
        ),
        "e. Calculate the volume of a Right Circular Cylinder": (
            calculate_cylinder_volume
        ),
        "f. Exit program": exit_program,
    }
    # calls the dict_menu() function from the prompt module.
    lab2prompt.Prompt.dict_menu(options)


if __name__ == "__main__":
    main()
