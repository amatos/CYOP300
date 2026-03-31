"""
Author: Alberth Matos
CYOP300
Date: 31 March 2026
Description: Functions to modify the state population data. Re-uses the
search_states module for selection of states.

The modify_state_population function allows for updating the population of a
state and optionally saving the changes to persistent state data in the form
of an alternate 'modified_us_states.csv' file, saved via a call to
lab3states.States().write_state_data().

As noted in the documentation for lab3states.States(), whenever the class is
loaded, it checks for the existence of 'modified_us_states.csv', and loads
that file if it is found.
"""

try:
    import lab3common
    import lab3prompt
    import lab3search_states
    import lab3states
    import lab3graph
except ImportError:
    from . import lab3common
    from . import lab3prompt
    from . import lab3search_states
    from . import lab3states
    from . import lab3graph


def modify_by_abbrev() -> None:
    """
    Modify the population data of a state retrieved by its abbreviation.

    :return: None
    :rtype: None
    """
    state = lab3search_states.search_by_abbrev()
    modify_state_population(state)


def modify_by_name() -> None:
    """
    Modifies the population of a state identified by its name.

    :return: None
    :rtype: None
    """
    state = lab3search_states.search_by_name()
    modify_state_population(state)


def modify_from_list() -> None:
    """
    Modify a state's population based on a user-selected list of states.

    :return: None
    :rtype: None
    """
    state = lab3search_states.choose_from_list()
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
    states = lab3states.States()
    if state:
        print(f"Current population of {state['state']}: {int(state['population']):,}")
        new_population = lab3common.get_input(int, "Enter the new population: ")
        state["population"] = new_population
        print(f"New population of {state['state']}: {int(state['population']):,}")
        print("N.b., you must save the changes in order to persist them.")
        print("They will otherwise be discarded when leaving this function")
        save_changes = lab3common.get_yes_no_input(prompt="Save changes? (y/n): ")
        for s in states:
            if s["state"].lower() == state["state"].lower():
                s["population"] = state["population"]
        if save_changes.lower() == "y":
            states.write_state_data(states.state_data)
    else:
        print("State not found. Cannot modify population.")
