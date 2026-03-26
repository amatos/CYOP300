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

from typing import TypeVar, Type

T = TypeVar("T")


def get_input(input_type: Type[T], prompt: str) -> T:
    """
    Prompts for user input, converts it to the specified type, and handles invalid inputs.

    :param input_type: The desired type to which the user's input should be converted.
    :type input_type: type
    :param prompt: The message displayed to the user when requesting input.
    :type prompt: str
    :return: The user's input converted to the specified type.
    :rtype: Any
    """
    while True:
        user_input = input(prompt)
        try:
            return input_type(user_input)
        except ValueError:
            print(f"Invalid input. Please enter a valid {input_type.__name__}.")


def get_yes_no_input(prompt: str) -> str:
    """Prompt until the user enters 'y' or 'n'.

    :param prompt: The type or designation of the dimension being entered (e.g., 'length', 'width').
    :type value_type: str
    :return: The user's response (either 'y' or 'n').
    :rtype: str
    """
    response = get_input(str, prompt).lower()
    while response not in ("y", "n"):
        print("Invalid input. Please enter 'y' or 'n'.")
        response = get_input(str, prompt).lower()
    return response


def get_input_in_mm(value_type: str, object_prompt: str) -> tuple[float, str]:
    """
    The function converts units of distance (km, m, cm, mm) into millimeters
    and adjusts the output value accordingly. If an invalid unit is provided,
    the input process is repeated until valid data is entered.

    :param value_type: The type or designation of the dimension being entered
                       (e.g., 'length', 'width').
    :type value_type: str
    :param object_prompt: A descriptor to display when prompting the user for
                          the value.
    :type object_prompt: str
    :return: A tuple where the first element is the converted value in
             millimeters and the second is the original unit provided by the user.
    :rtype: tuple[float, str]
    """
    while True:
        value = get_input(float, f"Please enter the {object_prompt}: ")
        value_type_unit = get_input(
            str, f"Please enter the unit of the {value_type} (km, m, cm, mm): "
        ).lower()
        if value_type_unit == "km":
            value *= 1000
            break
        if value_type_unit == "m":
            break
        if value_type_unit == "cm":
            value *= 0.1
            break
        if value_type_unit == "mm":
            value *= 0.01
            break
        print(f"Invalid {value_type} unit. Please enter km, m, cm, or mm.")
    return value, value_type_unit
