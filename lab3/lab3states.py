"""
Author: Alberth Matos
CYOP300
Date: 31 March 2026
Description: Contains the States() class, which is responsible for loading,
storing, and managing the state data from a CSV file. The class provides
methods for retrieving state information by abbreviation or name, as well as
updating the population of a state and saving changes to a modified CSV file.

The class also ensures that the state data is sorted alphabetically by state
name when loaded.

When data is loaded from the CSV file, the class checks to see if a modified
version of the states data file exists (as modified_us_states.csv), and, if it
does, it loads that file. Otherwise, it will load us_states.csv. This allows
for an easy way to reset the data back to the 2020 census data.
"""

import csv
import os


class States:
    """
    Represents a collection of U.S. states and provides functionality for accessing,
    modifying, and managing state-related data.

    This class is designed to handle state information by loading it from a
    CSV file, providing methods to retrieve specific state details based on
    name or abbreviation, updating population information, and writing updated
    data back to a file. The data handling includes case-insensitive lookups
    and ensures data integrity by sorting and storing the information consistently.

    :ivar state_data: A sorted list of dictionaries where each dictionary represents
        state information. Loaded from a CSV file during initialization.
    :type state_data: list[dict[str, str]]
    """

    def __init__(self) -> None:
        """
        Initialize a class instance by loading the necessary state data.

        :Attributes:
            - state_data: Dict
              Represents the loaded state data necessary for the
              instance's functionality. This is set during initialization.
        """
        self.state_data = self.load_state_data()

    def __getitem__(self, item: int) -> dict[str, str]:
        """
        Retrieve an item from the internal state data based on the given key or index.

        :param item: The key or index used to retrieve the corresponding value from
            the internal state data.
        :type item: Any
        :return: The value associated with the provided key or index from the
            internal state data.
        :rtype: Any
        """
        return self.state_data[item]

    @staticmethod
    def load_state_data() -> list[dict[str, str]]:
        """
        Load state data from a CSV file.

        There are two candidate files that we can load:
            - us_states.csv : The initial data file, sorted by the shortest
              line first, used to prove that we are sorting the resulting list
              alphabetically by state name.
            - us_states_modified.csv : An optional file created if the user
              modifies any data.

        The program will check for the existence of the modified file, and,
        if it exists, load it. Otherwise, the program will load the original
        unmodified file.
        :return: sorted_reader
        :rtype: list
        """
        if os.path.exists(os.path.join("data", "us_states_modified.csv")):
            filename = os.path.join("data", "us_states_modified.csv")
        else:
            filename = os.path.join("data", "us_states.csv")
        with open(file=filename, mode="r", encoding="utf-8") as file:
            # Load the CSV file into a list of dictionaries
            reader = csv.DictReader(file)
            # Create a new list of dictionaries sorted by the "state" key,
            # using a lambda function.
            sorted_reader = sorted(reader, key=lambda row: row["state"])
        # Return the resulting sorted list of dictionaries.
        return list(sorted_reader)

    @staticmethod
    def write_state_data(states_data: list[dict[str, str]]):
        """
        Write state data to a CSV file.

        :param states_data:
        :type states_data:
        :return: None
        :rtype: None
        """
        filename = os.path.join("data", "us_states_modified.csv")
        with open(file=filename, mode="w", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=states_data[0].keys())
            writer.writeheader()
            writer.writerows(states_data)

    def get_state_by_abbreviation(self, state_abbrev: str) -> dict[str, str] | None:
        """
        Retrieves state information based on the provided state abbreviation,
        ignoring case sensitivity. If a match is found, the method returns
        the corresponding state information. Otherwise, it returns None.

        :param state_abbrev: The abbreviation of the state to search for.
        :type state_abbrev: str
        :return: A dictionary containing the state information if a match is found,
            or None if no match is found.
        :rtype: dict[str, str] | None
        """
        # Searches through the class attribute, state_data, for a state with
        # a matching abbreviation. Both the passed state_abbrev and the
        # individual s["abbreviation"] are converted to lowercase to ensure
        # that the search is case-insensitive.
        state = [
            s
            for s in self.state_data
            if s["abbreviation"].lower() == state_abbrev.lower()
        ]
        # If a match is found, return the first element of the list. Otherwise,
        # return None. Since the state abbreviations are unique, this is always
        # guaranteed to return either a single resulting dictionary or None.
        return state[0] if state else None

    def get_state_by_name(self, state_name: str) -> dict[str, str] | None:
        """
        Retrieves state information based on the provided state name,
        ignoring case sensitivity. If a match is found, the method returns
        the corresponding state information. Otherwise, it returns None.

        :param state_name: The name of the state to search for.
        :type state_name: str
        :return: A dictionary containing the state information if a match is found,
            or None if no match is found.
        :rtype: dict[str, str] | None
        """
        # Searches through the class attribute, state_data, for a state with
        # a matching name. Both the passed state_name and the individual
        # s["name"] are converted to lowercase to ensure that the search is
        # case-insensitive.
        state = [s for s in self.state_data if s["state"].lower() == state_name.lower()]
        # If a match is found, return the first element of the list. Otherwise,
        # return None. Since the state abbreviations are unique, this is always
        # guaranteed to return either a single resulting dictionary or None.
        return state[0] if state else None

    def update_state_population(self, state_name: str, new_population: int) -> bool:
        """
        Updates the population of a specified state if it exists in the state data.

        This function iterates through the list of state data to find a state
        that matches the given state name (case-insensitive). If the state is
        found, it updates its population value to the new value provided. If
        the specified state is not found, the function returns False.

        :param state_name: The name of the state whose population is to be updated.
        :type state_name: str
        :param new_population: The new population value to assign to the state.
        :type new_population: int
        :return: True if the population was successfully updated, False otherwise.
        :rtype: bool
        """
        for state in self.state_data:
            if state["state"].lower() == state_name.lower():
                state["population"] = str(new_population)
                self.write_state_data(self.state_data)
                return True
        return False
