"""
Author: Alberth Matos
CYOP300
Date: 14 April 2026
Description: This module contains the main user interface as well as the core
logic for analyzing the datasets.

The initial plan was to implement only the UI components in this module, and
isolate the data analysis logic into another module, however, both compute_statistics()
and display_historygram() were so simple that it seemed easier to just combine
both elements here.

"""

from typing import Optional, List
from InquirerPy import inquirer
from matplotlib import pyplot
import pandas as pd


def lab5ui(
    pop_data: Optional[pd.DataFrame], housing_data: Optional[pd.DataFrame]
) -> None:
    """
    Provides a user interface for analyzing population and housing datasets.
    Users can interactively select a dataset and perform operations on it
    using the user interface.

    :param pop_data: The population dataset to be analyzed. It is expected to
        be a pandas DataFrame with relevant population data.
    :type pop_data: Optional[pandas.DataFrame]
    :param housing_data: The housing dataset to be analyzed. It is expected
        to be a pandas DataFrame containing details of housing data.
    :type housing_data: Optional[pandas.DataFrame]
    :return: None
    :rtype: None
    """
    # Initialize variables
    columns = []
    dataframe = None
    # Print top-line header
    print("***************** Welcome to the Python Data Analysis App **********")
    while True:
        # Prompt user to select a dataset to analyze
        file_to_analyze = inquirer.select(
            message="Select the file you want to analyze:",
            choices=["Population Data", "Housing Data", "Exit"],
            vi_mode=True,
        ).execute()

        # If the user selects "Exit", exit the program with a goodbye message
        if file_to_analyze == "Exit":
            print(
                "\n\n*************** Thanks for using the Data Analysis App **********"
            )
            return
        # If the user selects a dataset, populate 'columns' with the
        # appropriate column names, and populate the dataset into `dataframe`.
        if file_to_analyze == "Population Data":
            columns = ["a. Pop Apr 1", "b. Pop Jul 1", "c. Change Pop", "d. Exit"]
            dataframe = pop_data
        if file_to_analyze == "Housing Data":
            columns = [
                "a. AGE",
                "b. BEDRMS",
                "c. BUILT",
                "d. ROOMS",
                "e. UTILITY",
                "f. Exit",
            ]
            dataframe = housing_data
        # Call select_dataset_column() to start the analysis of the dataset.
        select_dataset_column(
            dataframe=dataframe, columns=columns, dataset_name=file_to_analyze
        )


def select_dataset_column(
    dataframe: pd.DataFrame, columns: List[str], dataset_name: str
) -> None:
    """
    Provides a menu-based interface for analyzing columns in a dataset. Users
    can iteratively select columns to analyze their statistics and generate
    histograms for visualization. The menu allows navigation and provides an
    exit option when the analysis is complete.

    :param dataframe: The pandas DataFrame containing the dataset to analyze.
    :type dataframe: pd.DataFrame
    :param columns: A list of strings representing the names of the columns
        available for analysis.
    :type columns: List[str]
    :param dataset_name: The name of the dataset being analyzed, used for
        user-friendly display purposes.
    :type dataset_name: str
    :return: None
    :rtype: None
    """
    # Initialize variables
    col_name = ""

    while True:
        print(f"You have entered {dataset_name}.")
        # Prompt the user to select which column to analyze, or 'exit' to return
        # to the previous menu. N.b., unless the user selects 'Exit', the
        # analysis will continue looping.
        column_to_analyze = inquirer.select(
            message="Select the Column you want to analyze:",
            choices=columns,
            vi_mode=True,
        ).execute()

        # Column names are prefixed with a letter and a period (e.g.,
        # "a. Pop Apr 1"), so we slice off the first three characters to get
        # the actual column name.
        col_name = column_to_analyze[3:]
        # If the user selects "Exit", print a goodbye message and return to
        # the previous menu.
        if col_name == "Exit":
            print(f"Exiting {dataset_name} analysis.")
            return
        print(f"You selected: {col_name}")
        print("The statistics for this column are:")
        # Compute and display statistics for the selected column.
        compute_statistics(dataframe[col_name])
        print(f"\nThe Histogram of {col_name} is now displayed.")
        # Display a histogram for the selected column.
        display_histogram(dataframe[col_name], col_name, dataset_name)


def compute_statistics(series: pd.Series) -> None:
    """
    Computes and prints basic statistical metrics for a given pandas Series.

    This function calculates the count, mean, standard deviation, minimum, and
    maximum of the input pandas Series and prints them in a formatted output.

    :param series: The pandas Series object containing numerical data for which
        the statistics will be computed.
    :type series: pd.Series
    :return: None
    :rtype: None
    """
    # Use built-in pandas functions to compute and then print statistics
    count = series.count()
    mean = series.mean()
    std = series.std()
    minimum = series.min()
    maximum = series.max()

    # N.b., formatting was set to 1 decimal place, following the example in
    # the lab instructions.
    print(f"  Count              = {count}")
    print(f"  Mean               = {mean:.1f}")
    print(f"  Standard Deviation = {std:.1f}")
    print(f"  Min                = {minimum:.1f}")
    print(f"  Max                = {maximum:.1f}")


def display_histogram(series: pd.Series, column_name: str, dataset_name: str) -> None:
    """
    Displays a histogram for a given data series, providing a visual
    representation of the frequency distribution of the values in a specific
    column from a dataset.

    :param series: The data series for which the histogram is to be displayed.
        Null values are excluded before plotting.
    :type series: pd.Series
    :param column_name: Name of the column being visualized. Used in the
        graph's title and x-axis label.
    :type column_name: str
    :param dataset_name: Name of the dataset the column belongs to, included
        in the graph's title.
    :type dataset_name: str
    :return: Does not return a value. Displays the histogram plot and a
        confirmation message to the console.
    :rtype: None
    """
    # Use built-in matplotlib function to plot the histogram:
    #   excluding null values
    #   with bins set to 20
    #   with blue bars and black edges
    #   with a title, and labels for the x-axis and y-axis
    pyplot.figure(figsize=(8, 5))
    pyplot.hist(series.dropna(), bins=20, color="blue", edgecolor="black")
    pyplot.title(f"Histogram of {column_name}\n({dataset_name})", fontsize=14)
    pyplot.xlabel(column_name, fontsize=12)
    pyplot.ylabel("Frequency", fontsize=12)
    pyplot.tight_layout()
    pyplot.show()
