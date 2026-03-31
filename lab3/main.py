"""
Author: Alberth Matos
CYOP300
Date: 31 March 2026
Description:

1. Display all U.S. States in Alphabetical order along with the Capital, State Population, and Flower
2. Search for a specific state and display the appropriate Capital name, State Population, and an image of the associated State Flower.
3. Provide a Bar graph of the top 5 populated States showing their overall population.
4. Update the overall state population for a specific state.
5. Exit the program
"""

try:
    import lab3common
    import lab3prompt
    import lab3search_states
    import lab3states
    import lab3graph
    import lab3modify_pop
except ImportError:
    from . import lab3common
    from . import lab3prompt
    from . import lab3search_states
    from . import lab3states
    from . import lab3graph
    from . import lab3modify_pop

# from lab3.lab3states import States


def exit_program() -> None:
    """Exits the program.

    :return: None
    :rtype: None
    """
    lab3common.exit_program()


def display_states() -> None:
    """Displays all U.S. States in Alphabetical order along with the Capital, State Population, and Flower.

    :return: None
    :rtype: None
    """

    states = lab3states.States()
    print(
        "Displaying all U.S. States in Alphabetical order along with the Capital, State Population, and Flower."
    )

    for state in states.state_data:
        print(
            f"State: {state['state']}, Capital: {state['capital']}, Population: {int(state['population']):,}, Flower: {state['flower']}"
        )

    lab3prompt.reprompt_menu(display_states)


def search_states() -> None:
    """Searches for a specific state and displays the appropriate Capital name, State Population, and an image of the associated State Flower.

    :return: None
    :rtype: None
    """
    print(
        "Searching for a specific state and displaying the appropriate Capital name, State Population, and an image of the associated State Flower."
    )
    # Define the menu options and their corresponding functions in a dictionary.
    options = {
        "Search State by abbreviation": lab3search_states.display_by_abbrev,
        "Search State by name": lab3search_states.display_by_name,
        "Choose State from a menu": lab3search_states.display_from_list,
    }
    # calls the dict_menu() function from the prompt module.
    lab3prompt.Prompt.dict_menu(options)
    lab3prompt.reprompt_menu(search_states)


def graph_bar() -> None:
    """Provides a Bar graph of the top 5 populated States showing their overall population.

    :return: None
    :rtype: None
    """
    print(
        "Providing a Bar graph of the top 5 populated States showing their overall population."
    )
    lab3graph.plot_top_5_state_populations()
    lab3prompt.reprompt_menu(graph_bar)


def update_state_population() -> None:
    """Updates the overall state population for a specific state.

    :return: None
    :rtype: None
    """
    print("Updating the overall state population for a specific state.")
    print("Select the State you want to update:")
    options = {
        "Enter State by abbreviation": lab3modify_pop.modify_by_abbrev,
        "Enter State by name": lab3modify_pop.modify_by_name,
        "Choose State from a menu": lab3modify_pop.modify_from_list,
    }
    # calls the dict_menu() function from the prompt module.
    lab3prompt.Prompt.dict_menu(options)
    lab3prompt.reprompt_menu(update_state_population)


def main():
    """
    This is the main function that serves as the entry point for the program.
    It provides a menu-driven interface using TerminalMenu (see lab2prompt.py
    for implementation), which allows users to select from a set of tasks
    as required by the Lab documentation.

    :return: None
    :rtype: None
    """

    # Clears the screen and moves the cursor to the top-left corner using ANSI escape codes.
    print("\033[H\033[2J", end="", flush=True)
    print("Welcome to Lab 3. Please select from one of the following options:")
    # Define the menu options and their corresponding functions in a dictionary.
    options = {
        "1. Display all U.S. States in Alphabetical order along with the Capital, State Population, and Flower": (
            display_states
        ),
        "2. Search for a specific state and display the appropriate Capital name, State Population, and an image of the associated State Flower.": (
            search_states
        ),
        "3. Provide a Bar graph of the top 5 populated States showing their overall population.": (
            graph_bar
        ),
        "4. Update the overall state population for a specific state.": (
            update_state_population
        ),
        "5. Exit the program": lab3common.exit_program,
    }
    # calls the dict_menu() function from the prompt module.
    lab3prompt.Prompt.dict_menu(options)


if __name__ == "__main__":
    main()
