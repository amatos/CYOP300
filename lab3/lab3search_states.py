"""
Author: Alberth Matos
CYOP300
Date: 31 March 2026
Description: Functions to allow a user to search and display data for a state
in one of three forms:
    1. Search by state abbreviation
    2. Search by state name
    3. Choose from a list of states

The display functions will show the state name, capital, population, and an
image of the state flower. The data and image of the state flower is sourced
from https://statesymbolsusa.org/categories/flower. The state capital and name
of the flower was sourced from:
https://www.crestcapital.com/tax/us_states_and_capitals
"""

from term_image.image import from_file
import os
from typing import Optional

try:
    import lab3common
    import lab3prompt
    import lab3states
    import lab3graph
    import lab3modify_pop
except ImportError:
    from . import lab3common
    from . import lab3prompt
    from . import lab3states
    from . import lab3graph
    from . import lab3modify_pop


def search_by_abbrev() -> Optional[dict]:
    """
    Searches for a U.S. state by its abbreviation and returns the corresponding state
    object if found. If the abbreviation is invalid, the function informs the user and
    offers options to retry, return to the main menu, or exit.

    :return: The state object corresponding to the provided abbreviation, or None if
        the abbreviation is invalid or the user chooses not to retry.
    :rtype: Optional[lab3states.State]
    """
    # Create an instance of the States class.
    states = lab3states.States()
    # Prompt the user to enter a state abbreviation.
    state_abbrev = lab3common.get_input(str, "Enter the state abbreviation: ")
    # Validate the state abbreviation and retrieve the corresponding state object.
    state = states.get_state_by_abbreviation(state_abbrev)
    # lab3states.States().get_state_by_abbreviation() will return None if the
    # abbreviation is invalid. We use this as a check to validate the user
    # input. If the check fails, we inform the user and offer options to either
    # retry, return to the main menu, or exit.
    if not state:
        print("Invalid state abbreviation.")
        print("Would you like to try again, return to the main menu, or exit?")
        return None
    # Return the state dictionary to the calling function.
    return state


def search_by_name() -> Optional[dict]:
    """
    Searches for a state by its name and retrieves its corresponding
    representation. If the state name is invalid, the user is notified and
    prompted to decide whether to try searching again, return to the main
    menu, or exit. The function uses user-provided input to perform the search.

    :return: The state representation corresponding to the given name, or
             None if no valid state is found or if the user chooses to exit
             or return to the main menu.
    :rtype: State or None
    """
    # Create an instance of the States class.
    states = lab3states.States()
    # Prompt the user to enter a state name.
    state_name = lab3common.get_input(str, "Enter the state name: ")
    # Validate the state name and retrieve the corresponding state object.
    state = states.get_state_by_name(state_name)
    # lab3states.States().get_state_by_name() will return None if the state
    # name is invalid.
    if not state:
        print("Invalid state name.")
        print("Would you like to try again, return to the main menu, or exit?")
        return None
    # Return the state dictionary to the calling function.
    return state


def choose_from_list() -> Optional[dict]:
    """
    Allows a user to select a state from a predefined list of options. The chosen
    state is then retrieved and returned as a dictionary containing its
    details.

    :return: A dictionary containing details of the selected state, or None
             if no valid selection is made.
    :rtype: Optional[dict]
    """
    # Create an instance of the States class.
    states = lab3states.States()
    # Define the states in a list.
    options = [
        "Alabama",
        "Alaska",
        "Arizona",
        "Arkansas",
        "California",
        "Colorado",
        "Connecticut",
        "Delaware",
        "Florida",
        "Georgia",
        "Hawaii",
        "Idaho",
        "Illinois",
        "Indiana",
        "Iowa",
        "Kansas",
        "Kentucky",
        "Louisiana",
        "Maine",
        "Maryland",
        "Massachusetts",
        "Michigan",
        "Minnesota",
        "Mississippi",
        "Missouri",
        "Montana",
        "Nebraska",
        "Nevada",
        "New Hampshire",
        "New Jersey",
        "New Mexico",
        "New York",
        "North Carolina",
        "North Dakota",
        "Ohio",
        "Oklahoma",
        "Oregon",
        "Pennsylvania",
        "Rhode Island",
        "South Carolina",
        "South Dakota",
        "Tennessee",
        "Texas",
        "Utah",
        "Vermont",
        "Virginia",
        "Washington",
        "West Virginia",
        "Wisconsin",
        "Wyoming",
    ]
    option_choice = lab3prompt.Prompt.menu(options)
    # Retrieve the state dictionary corresponding to the chosen option.
    state = states.get_state_by_name(option_choice)
    # Return the state dictionary to the calling function.
    return state


def display_state(state_abbrev: str) -> None:
    """
    This function retrieves state information such as name, capital, population,
    and flower based on the given state abbreviation. It also attempts to display
    an image associated with the state flower. If the state abbreviation is invalid
    or the flower image is unavailable, appropriate messages are displayed.

    The state abbreviation is used as the key for two reasons:
        1. Known unique value that is easy to type while testing.
        2. Simplify the code by using the abbreviation as the filename for
           the image.


    :param state_abbrev: The two-letter abbreviation of the state.
    :type state_abbrev: str
    :return: None
    :rtype: None
    """
    # Create an instance of the States class.
    states = lab3states.States()
    # Get the state dictionary object based on the passed state abbreviation.
    state = states.get_state_by_abbreviation(state_abbrev)
    # If the state abbreviation returns a dictionary, we can access the
    # state's capital, population, and flower using the keys.
    if not state:
        print("Invalid state abbreviation.")
        print("Would you like to try again, return to the main menu, or exit?")
        return
    # We build the path to the state flower image based on the state abbreviation.
    # The image files sourced from statesymbolsusa.org were renamed to
    # correspond to the state abbreviation for ease of use and quick sanity
    # checking.
    state_flower = os.path.join("images", state["abbreviation"] + ".jpg")
    # While this should never occur, we check for the existence of the image
    # file anyway, and display a message if the image does not exist.
    if not os.path.exists(state_flower):
        print("No image found for this state.")
        return
    # Load the image data using term_image.image.from_file() and display the
    # image in the terminal.m
    image = from_file(state_flower)
    image.draw()
    # Finally, we print the state information, including the state name,
    # capital, population (formatted with commas), and flower name.
    print(
        f'State: {state["state"]}, Capital: {state["capital"]}, '
        f'Population: {int(state["population"]):,}, Flower: {state["flower"]}'
    )


def display_by_abbrev() -> None:
    """
    Displays information for a state based on its abbreviation. Calls
    search_by_abbrev() to retrieve the state data.

    This was split off from search_by_abbrev() to allow recycling of the
    function by lab3.main

    :return: None
    :rtype: None
    """
    state = search_by_abbrev()
    if state:
        display_state(state["abbreviation"])
    lab3prompt.reprompt_menu(display_by_abbrev)


def display_by_name() -> None:
    """
    Searches for a state by its name, displays its corresponding abbreviation if found,
    and reprompts the user for further actions if necessary.

    This was split off from search_by_abbrev() to allow recycling of the
    function by lab3.main

    :return: None
    :rtype: None
    """
    state = search_by_name()
    if state:
        display_state(state["abbreviation"])
    lab3prompt.reprompt_menu(display_by_name)


def display_from_list() -> None:
    """
    Displays a state abbreviation after selection from a list.

    This was split off from search_by_abbrev() to allow recycling of the
    function by lab3.main

    :return: None
    :rtype: None
    """
    state = choose_from_list()
    display_state(state["abbreviation"])
    lab3prompt.reprompt_menu(display_from_list)
