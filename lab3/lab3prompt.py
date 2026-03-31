"""
Author: Alberth Matos
CYOP300
Date: 31 March 2026
Description: Provides a menu-driven terminal interface for my Lab3 application.
  The _Prompt class contains two static methods: menu() and dict_menu().

  The menu() method takes a list of options and displays them in a terminal
  menu, allowing the user to select one.
  The dict_menu() method takes a dictionary of options, displays the keys as a
  menu, and executes the corresponding function based on the user's selection.
"""

from collections.abc import Callable
from simple_term_menu import TerminalMenu

try:
    import lab3common
    import lab3search_states
    import lab3states
    import lab3graph
    import lab3modify_pop
except ImportError:
    from . import lab3common
    from . import lab3search_states
    from . import lab3states
    from . import lab3graph
    from . import lab3modify_pop


class Prompt:
    """
    This class serves as a utility for providing interactive terminal menus and enabling
    the execution of functions based on user-selected options.

    :ivar options: A list of options used to populate menu selections.
    :type options: list
    """

    def __init__(self, options):
        self.options = options

    @staticmethod
    def menu(options: list) -> str:
        """
        Displays a terminal-based menu and returns the user's selection.

        :param options: List of options to display in the menu.
        :type options: list

        :return: The option selected by the user.
        :rtype: str
        """

        terminal_menu = TerminalMenu(options)
        menu_entry_index = terminal_menu.show()
        selection = options[menu_entry_index]
        return selection

    @staticmethod
    def dict_menu(dict_options: dict[str, Callable[[], None]]) -> None:
        """
        Execute a function mapped to a choice in a dictionary.

        This function takes a dictionary where the keys represent menu options
        and the values are callable functions. Using the `Prompt.menu' method,
        it prompts the user to select an option from the menu. Once a
        selection is made, the function corresponding to the selected option
        is invoked.

        :param dict_options: A dictionary mapping string menu options to callable
            functions.
        :type dict_options: dict[str, Callable[[], None]]

        :return: None
        :rtype: None
        """

        selection = Prompt.menu(list(dict_options))
        selected_function = dict_options.get(selection)
        selected_function()


def reprompt_menu(caller_name: Callable[[], None]) -> None:
    """Re-prompts the user for a valid input based on the provided menu item."""

    from main import main

    print("")
    options = {
        "Try Again": caller_name,
        "Return to Main Menu": main,
        "Exit": lab3common.exit_program,
    }
    Prompt.dict_menu(options)
