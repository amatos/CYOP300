"""
Author: Alberth Matos
CYOP300
Date: 07 April 2026
Description: This module serves as the starting point for 'the Python Matrix
Application', Lab 4. The lab demonstrates the usage of NumPy arrays and matrix
operations, along with the use of Pandas for data analysis.
"""

from matrix_game import play_matrix_game


def main() -> None:
    """
    This function serves as the starting point for 'the Python Matrix Application'. It
    provides a user interface loop for the user to decide whether to play the Matrix
    Game or exit the application.

    :return: None
    :rtype: None
    """
    print("*" * 20 + " Welcome to the Python Matrix Application " + "*" * 20)

    while True:
        print("Do you want to play the Matrix Game?")
        play = input("Enter Y for Yes or N for No: ").strip().lower()

        if play == "y":
            play_matrix_game()
        elif play == "n":
            print("*" * 15 + " Thanks for playing Python NumPy " + "*" * 15)
            break
        else:
            print("Invalid input. Please enter Y or N.")


if __name__ == "__main__":
    main()
