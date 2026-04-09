"""
Author: Alberth Matos
CYOP300
Date: 07 April 2026
Description: This module implements the 'Matrix Game' as part of Lab 4,
containing the usage of NumPy and Pandas for matrix operations.

This module is called by main.py, and, in turn, calls phone_and_zip.py get and
validate phone and zip code data.
"""

import numpy as np
import pandas as pd

from phone_and_zip import get_phone, get_zipcode


def parse_matrix_row(row_str: str) -> list[float] | None:
    """
    Parse a single row of a matrix from a string, validating its format and
    converting its elements into floating point numbers if they are integers.
    A valid row must contain exactly three tokens that can be converted into
    floats. If the string is invalid or contains non-convertible values, the
    function returns None. If the string is valid, return a list of three floats.

    :param row_str: A string representing a single row of a matrix, with elements
        separated by whitespace.
    :type row_str: str
    :return: A list of three floating-point numbers parsed from the input string
        if valid, or None if the input string is invalid.
    :rtype: list[float] | None
    """
    # Split the string into tokens, split by whitespace.
    tokens = row_str.strip().split()
    # If the number of tokens is NOT 3, return None.
    if len(tokens) != 3:
        return None
    # Initialize an empty list to contain the floats
    values = []
    # Parse each token, append them as a float to values. If a token cannot
    # be parsed as a float, catch the exception and return None.
    for token in tokens:
        try:
            values.append(float(token))
        except ValueError:
            return None
    # Finally, return the list of floats.
    return values


def get_matrix(label: str) -> np.ndarray:
    """
    This function repeatedly requests input for each row of the matrix until
    a valid numeric input is provided. Each row must consist of exactly
    three numeric values separated by whitespaces. The function uses a helper
    function, parse_matrix_row(), to validate the inputs and convert them to
    a list of floats.

    :param label: A descriptive label to display during input prompts,
        indicating the purpose of the matrix being entered (e.g., "A").
    :type label: str
    :return: A 3x3 NumPy array containing the entered matrix.
    :rtype: numpy.ndarray
    """
    print(f"Enter your {label} 3x3 matrix:")
    rows = []
    while len(rows) < 3:
        row_input = input(f"Enter row {len(rows) + 1} for {label}: ").strip()
        parsed = parse_matrix_row(row_input)
        if parsed is None:
            print("Invalid input. Please enter 3 numeric values separated by spaces.")
        else:
            rows.append(parsed)
    return np.array(rows)


def display_matrix(matrix: np.ndarray, label: str = "") -> None:
    """
    This function takes a matrix and formats its output using pandas for a
    cleaner display. If all values in the matrix are integers, they are
    displayed without decimals. Otherwise, floating-point values are shown
    with two decimal places. The index and column headers of the matrix
    are omitted in the display. An optional label can also be provided for
    the output.

    :param matrix: The matrix to be displayed.
    :type matrix: np.ndarray
    :param label: A label to describe or annotate the displayed matrix.
        Defaults to an empty string.
    :type label: str
    :return: None
    :rtype: None
    """
    if label:
        print(label)
    # Use pandas DataFrame for clean formatting (integers shown without
    # decimals where possible)
    df = pd.DataFrame(matrix)
    # Format: show as int if all values are whole numbers, else as floats
    if np.all(matrix == matrix.astype(int)):
        formatted = df.map(lambda x: str(int(x)))
    else:
        formatted = df.map(lambda x: f"{x:.2f}")
    # Print without index or column headers
    print(formatted.to_string(index=False, header=False))


def matrix_add(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """
    This function performs an element-wise addition of two NumPy arrays, a and b.
    The input arrays must have the same shape for the operation to be successful.

    :param a: The first input matrix for the addition operation.
    :type a: numpy.ndarray
    :param b: The second input matrix for the addition operation.
    :type b: numpy.ndarray
    :return: The resulting matrix after element-wise addition of a and b.
    :rtype: numpy.ndarray
    """
    return np.add(a, b)


def matrix_subtract(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """
    This function performs element-wise subtraction of two matrices
    represented as NumPy arrays. Both input matrices must have the same
    dimensions to perform the operation.

    :param a: The first input matrix.
    :type a: np.ndarray
    :param b: The second input matrix to subtract from the first.
    :type b: np.ndarray
    :return: A matrix resulting from the element-wise subtraction of b from a.
    :rtype: np.ndarray
    """
    return np.subtract(a, b)


def matrix_multiply(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """
    This function takes two NumPy arrays as input and performs the standard
    matrix multiplication using NumPy's matmul function. Both input arrays
    should have dimensions compatible with matrix multiplication.

    :param a: The first input matrix.
    :type a: numpy.ndarray
    :param b: The second input matrix.
    :type b: numpy.ndarray
    :return: The result of the matrix multiplication.
    :rtype: numpy.ndarray
    """
    return np.matmul(a, b)


def matrix_element_multiply(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """
    This function takes two numpy arrays and performs element-wise multiplication.
    Both input matrices must have the same dimensions.

    :param a: The first matrix for element-wise multiplication.
    :type a: np.ndarray
    :param b: The second matrix for element-wise multiplication.
    :type b: np.ndarray
    :return: A matrix resulting from the element-wise multiplication of the
    input matrices.
    :rtype: np.ndarray
    """
    return np.multiply(a, b)


def get_operation_choice() -> str:
    """
    This function displays a list of matrix operations for the user to choose
    from, including addition, subtraction, matrix multiplication, and
    element-by-element multiplication. It prompts the user for their choice
    and ensures that the input is valid by checking against a set of acceptable
    options.

    :return: The user's valid choice, 'a', 'b', 'c', or 'd', corresponding to
        the selected matrix operation.
    :rtype: str
    """
    menu = (
        "Select a Matrix Operation from the list below:\n"
        "  a. Addition\n"
        "  b. Subtraction\n"
        "  c. Matrix Multiplication\n"
        "  d. Element by element multiplication"
    )
    print(menu)
    valid_choices = {"a", "b", "c", "d"}
    choice = input("Enter your choice (a/b/c/d): ").strip().lower()
    while choice not in valid_choices:
        print("Invalid choice. Please enter a, b, c, or d.")
        choice = input("Enter your choice (a/b/c/d): ").strip().lower()
    return choice


def display_results(result: np.ndarray, operation_name: str) -> None:
    """
    Displays the results of a matrix operation, including the operation
    performed, the matrix transpose, and the mean values of rows and columns.
    The results are printed formatted to two decimal places.

    :param result: The resulting matrix from the performed operation.
    :type result: np.ndarray
    :param operation_name: The name of the operation that produced the
        resulting matrix.
    :type operation_name: str
    :return: None
    :rtype: None
    """
    print(f"You selected {operation_name}. The results are:")
    display_matrix(result)

    # Transpose.
    transpose = result.T
    print("The Transpose is:")
    display_matrix(transpose)

    # Row means (mean across columns for each row).
    row_means = np.mean(result, axis=1)
    # Column means (mean across rows for each column).
    col_means = np.mean(result, axis=0)

    # Format mean values to 2 decimal places.
    row_str = ", ".join(f"{v:.2f}" for v in row_means)
    col_str = ", ".join(f"{v:.2f}" for v in col_means)

    # Print out the mean values, formatted to be more readable.
    print("The row and column mean values of the results are:")
    print(f"  Row means    : {row_str}")
    print(f"  Column means : {col_str}")


def play_matrix_game() -> None:
    """
    Plays a matrix game by allowing the user to input data, select a matrix
    operation, and display the results accordingly. This function serves as
    the main controller for managing user interaction and applying the chosen
    mathematical operations on matrices.

    :return: None. The function primarily produces output to the console
        during its execution.
    :rtype: NoneType
    """

    phone = get_phone()
    print(f"Phone number accepted: {phone}")

    zipcode = get_zipcode()
    print(f"Zip code accepted: {zipcode}")

    matrix_a = get_matrix("first")
    print("Your first 3x3 matrix is:")
    display_matrix(matrix_a)

    matrix_b = get_matrix("second")
    print("Your second 3x3 matrix is:")
    display_matrix(matrix_b)

    choice = get_operation_choice()

    operation_map = {
        "a": ("Addition", matrix_add),
        "b": ("Subtraction", matrix_subtract),
        "c": ("Matrix Multiplication", matrix_multiply),
        "d": ("Element by Element Multiplication", matrix_element_multiply),
    }

    operation_name, operation_func = operation_map[choice]
    result = operation_func(matrix_a, matrix_b)

    display_results(result, operation_name)
