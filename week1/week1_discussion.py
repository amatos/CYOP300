"""
Author: Alberth Matos
CYOP300
Date: 17 March 2026
Description: Sample program to demonstrate pylint
"""

import sys


def main():
    """
    Main function to run the program
    """
    return_code = 0
    print("Please enter your name: ")
    name = input()
    print(f"Hello, World that is inhabited by {name}!")
    print("What is your quest?")
    quest = input()
    print(f"Your quest is: {quest.lower()}")
    print("What is pi to the seventh decimal place?")
    pi = input()
    if pi == "3.1415926":
        print("Correct!")
    else:
        print("Incorrect!")
        return_code = 1
    sys.exit(return_code)


if __name__ == "__main__":
    main()
