"""
Author: Alberth Matos
CYOP300
Date: 31 March 2026
Description: This module handles the top-level functionality of the program,
including presenting the main menu, and execution of the top-level items.
"""

try:
    from lab3.lab3states import States
    from lab3.lab3search_states import (
        display_by_abbrev,
        display_by_name,
        display_from_list,
    )
    from lab3.lab3prompt import Prompt
    from lab3.lab3graph import plot_top_5_state_populations
    from lab3.lab3modify_pop import modify_by_abbrev, modify_by_name, modify_from_list
    from lab3.lab3common import exit_program, rerun_or_return
except ImportError as e:
    from lab3states import States
    from lab3search_states import display_by_abbrev, display_by_name, display_from_list
    from lab3prompt import Prompt
    from lab3graph import plot_top_5_state_populations
    from lab3modify_pop import modify_by_abbrev, modify_by_name, modify_from_list
    from lab3common import exit_program, rerun_or_return


def display_states(states: States) -> None:
    """Displays all U.S. States in Alphabetical order along with the Capital,
    State Population, and Flower.

    :return: None
    :rtype: None
    """

    print(
        "Displaying all U.S. States in Alphabetical order along with the "
        "Capital, State Population, and Flower."
    )
    for state in states.state_data:
        print(
            f"State: {state['state']}, Capital: {state['capital']}, "
            f"Population: {int(state['population']):,}, Flower: {state['flower']}"
        )
    selected_index = rerun_or_return()
    actions = {
        0: lambda: display_states(states),
        1: lambda: main_menu(states),
        2: lambda: exit_program(),
    }
    # Execute the associated action
    if selected_index in actions:
        actions[selected_index]()


def search_states(states: States) -> None:
    """Searches for a specific state and displays the appropriate Capital
    name, State Population, and an image of the associated State Flower.

    :return: None
    :rtype: None
    """
    print(
        "Searching for a specific state and displaying the appropriate Capital "
        "name, State Population, and an image of the associated State Flower."
    )
    # Define the menu options and their corresponding functions in a dictionary.
    options = [
        "Search State by abbreviation",
        "Search State by name",
        "Choose State from a menu",
    ]
    actions = {
        0: lambda: display_by_abbrev(states),
        1: lambda: display_by_name(states),
        2: lambda: display_from_list(states),
    }
    selected_index = Prompt.indexed_menu(options)
    # Execute the associated action
    if selected_index in actions:
        actions[selected_index]()

    selected_index = rerun_or_return()
    actions = {
        0: lambda: search_states(states),
        1: lambda: main_menu(states),
        2: lambda: exit_program(),
    }
    # Execute the associated action
    if selected_index in actions:
        actions[selected_index]()


def graph_bar(states: States) -> None:
    """Provides a Bar graph of the top 5 populated States showing their
    overall population.

    :return: None
    :rtype: None
    """
    print(
        "Providing a Bar graph of the top 5 populated States showing their "
        "overall population."
    )
    plot_top_5_state_populations(states)
    selected_index = rerun_or_return()
    actions = {
        0: lambda: graph_bar(states),
        1: lambda: main_menu(states),
        2: lambda: exit_program(),
    }
    # Execute the associated action
    if selected_index in actions:
        actions[selected_index]()


def update_state_population(states: States) -> None:
    """Updates the overall state population for a specific state.

    :return: None
    :rtype: None
    """
    print("Updating the overall state population for a specific state.")
    print("Select the State you want to update:")
    options = [
        "Enter State by abbreviation",
        "Enter State by name",
        "Choose State from a menu",
    ]
    actions = {
        0: lambda: modify_by_abbrev(states),
        1: lambda: modify_by_name(states),
        2: lambda: modify_from_list(states),
    }
    selected_index = Prompt.indexed_menu(options)
    # Execute the associated action
    if selected_index in actions:
        actions[selected_index]()

    selected_index = rerun_or_return()
    actions = {
        0: lambda: search_states(states),
        1: lambda: main_menu(states),
        2: lambda: exit_program(),
    }
    # Execute the associated action
    if selected_index in actions:
        actions[selected_index]()


def main_menu(states: States):
    """
    This is the main function that serves as the entry point for the program.
    It provides a menu-driven interface using TerminalMenu (see lab2prompt.py
    for implementation), which allows users to select from a set of tasks
    as required by the Lab documentation.

    :return: None
    :rtype: None
    """

    # Clears the screen and moves the cursor to the top-left corner using
    # ANSI escape codes.
    print("\033[H\033[2J", end="", flush=True)
    print("Welcome to Lab 3. Please select from one of the following options:")
    # Define the menu options and their corresponding functions in a dictionary.

    options = [
        "1. Display all U.S. States in Alphabetical order along with the "
        "Capital, State Population, and Flower",
        "2. Search for a specific state and display the appropriate Capital "
        "name, State Population, and an image of the associated State Flower.",
        "3. Provide a Bar graph of the top 5 populated States showing their "
        "overall population.",
        "4. Update the overall state population for a specific state.",
        "5. Exit the program",
    ]
    actions = {
        0: lambda: display_states(states),
        1: lambda: search_states(states),
        2: lambda: graph_bar(states),
        3: lambda: update_state_population(states),
        4: lambda: exit_program(),
    }
    selected_index = Prompt.indexed_menu(options)
    # Execute the associated action
    if selected_index in actions:
        actions[selected_index]()
