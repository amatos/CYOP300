"""
Author: Alberth Matos
CYOP300
Date: 14 April 2026
Description: The main entry point for the Lab 5 program. This module is
responsible for loading the necessary data, via a call to load_data.load_csv(),
and then passing the data and control to lab5ui.lab5ui(), which handles the
user interface.

"""

from os import getcwd
import sys
from typing import Optional
import pandas as pd

from load_data import load_csv
import lab5ui


def main() -> None:
    """
    This function attempts to load two CSV files: one for housing data and
    the other for population change data. If either file is not found, a
    message is displayed specifying the missing files, and the program
    terminates with an exit code of 1. Otherwise, the data is passed into
    a user interface module for further handling.

    :raises FileNotFoundError: If the required CSV files are not present
        in the current working directory.
    """
    # Initialize variables.
    housing_data: Optional[pd.DataFrame] = None
    pop_change_data: Optional[pd.DataFrame] = None
    pop_change_file: str = "PopChange.csv"
    housing_file: str = "Housing.csv"

    # Before doing anything else, attempt to load the required CSV files. If
    # either file is missing, generate an error message and exit the program.
    try:
        housing_data = load_csv(housing_file)
        pop_change_data = load_csv(pop_change_file)
    except FileNotFoundError:
        print(
            f"Both {housing_file} and {pop_change_file} are required. "
            f"Please ensure they are present in {getcwd()}."
        )
        sys.exit(1)

    # Once the data has been loaded, pass it to the user interface module.
    lab5ui.lab5ui(pop_data=pop_change_data, housing_data=housing_data)


if __name__ == "__main__":
    main()
