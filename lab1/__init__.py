"""
Author: Alberth Matos
CYOP300
Date:
Description: Defines a custom exception class for input validation errors.

This module includes the InputError class designed to handle issues related
to input validation. It extends from the built-in ValueError class and
provides additional context on the error by accepting a custom error message
during its initialization.

Classes:
- InputError: Represents input validation errors with custom messages.
"""


class InputError(ValueError):
    """
    Exception raised for errors in user input.

    This class is a custom exception that inherits from ValueError. It is
    designed to be used when user input validation fails. The exception
    is initialized with a message that provides details about the specific
    validation error.
    """
    def __init__(self, message: str) -> None:
        """
        Initialize the exception with a description of the input error.

        :param message: A message describing the validation failure.
        """
        super().__init__(message)


__all__ = ["InputError"]
