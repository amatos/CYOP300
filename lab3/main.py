"""
Author: Alberth Matos
CYOP300
Date: 31 March 2026
Description: This module is the main entry point for lab 3. It initializes the
States class, and then calls the main_menu function in lab3main.py, passing
the newly created States object as a parameter.

1. Display all U.S. States in Alphabetical order along with the Capital,
   State Population, and Flower.
2. Search for a specific state and display the appropriate Capital name,
   State Population, and an image of the associated State Flower.
3. Provide a Bar graph of the top 5 populated States showing their overall
   population.
4. Update the overall state population for a specific state.
5. Exit the program
"""

try:
    from lab3.lab3main import main_menu
    from lab3.lab3states import States
except ImportError as e:
    from lab3main import main_menu
    from lab3states import States


def main() -> None:
    """
    Initialize an instance of the States class. This class contains all of
    the data associated with the US States, and is passed to any functions
    that require it.

    :rtype: None
    """
    states = States()
    # Call the main_menu function, passing the newly created States object as
    # a parameter.
    main_menu(states)


if __name__ == "__main__":
    main()
