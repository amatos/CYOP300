"""
Author: Alberth Matos
CYOP300
Date: 31 March 2026
Description: Functions to modify the state population data. Re-uses the
search_states module for selection of states.

The modify_state_population function allows for updating the population of a
state and optionally saving the changes to persistent state data in the form
of an alternate `modified_us_states.csv' file, saved via a call to
`lab3states.States().write_state_data()'.

As noted in the documentation for `lab3states.States()', whenever the class is
loaded, it checks for the existence of `modified_us_states.csv', and loads
that file if it is found.
"""

try:
    from lab3.lab3common import get_input, get_yes_no_input
    from lab3.lab3search_states import (
        choose_from_list,
        search_by_abbrev,
        search_by_name,
    )
    from lab3.lab3states import States
except ImportError:
    from lab3common import get_input, get_yes_no_input
    from lab3search_states import choose_from_list, search_by_abbrev, search_by_name
    from lab3states import States


def modify_by_abbrev(states: States) -> None:
    """
    Modify the population data of a state retrieved by its abbreviation.

    :return: None
    :rtype: None
    """
    state = search_by_abbrev(states)
    modify_state_population(state)


def modify_by_name(states: States) -> None:
    """
    Modifies the population of a state identified by its name.

    :return: None
    :rtype: None
    """
    state = search_by_name(states)
    modify_state_population(state)


def modify_from_list(states: States) -> None:
    """
    Modify a state's population based on a user-selected list of states.

    :return: None
    :rtype: None
    """
    state = choose_from_list(states)
    modify_state_population(state)


def modify_state_population(state: dict | None) -> None:
    """
    Modifies the population value of a given state in the state data. The function allows
    for updating the population and optionally saving the changes to persistent state data.

    :param state: Dictionary representing the state whose population needs to be modified.
        The dictionary must contain keys 'state' and 'population'.
    :type state: dict | None
    :return: None
    :rtype: None
    """
    states = States()
    if state:
        print(f"Current population of {state['state']}: {int(state['population']):,}")
        new_population = get_input(int, "Enter the new population: ")
        state["population"] = new_population
        print(f"New population of {state['state']}: {int(state['population']):,}")
        print("N.b., you must save the changes in order to persist them.")
        print("They will otherwise be discarded when leaving this program.")
        save_changes = get_yes_no_input(prompt="Save changes? (y/n): ")
        for s in states:
            if s["state"].lower() == state["state"].lower():
                s["population"] = state["population"]
        if save_changes.lower() == "y":
            states.write_state_data(states.state_data)
    else:
        print("State not found. Cannot modify population.")
