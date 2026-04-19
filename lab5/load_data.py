"""
Author: Alberth Matos
CYOP300
Date: 14 April 2026
Description: helper module containing a function to load data from a CSV file
using pandas' read_csv() function. The function checks if the specified file
exists and returns a DataFrame if it does, or an FileNotFoundError exception
if the file does not exist.

"""

import os
from typing import Optional
import pandas as pd


def load_csv(filename: str) -> Optional[pd.DataFrame]:
    """
    This function attempts to read a CSV file and return it as a pandas
    DataFrame. If the file does not exist, a FileNotFoundError will be raised.

    :param filename: Path to the CSV file to be loaded.
    :type filename: str
    :return: A pandas DataFrame containing the contents of the CSV file.
    :rtype: Optional[pd.DataFrame]
    :raises FileNotFoundError: If the file specified by the filename does
        not exist.
    """
    # Check if file exists before attempting to read it, and raise
    # FileNotFoundError if it does not.
    if not os.path.exists(filename):
        raise FileNotFoundError
    return pd.read_csv(filename)
