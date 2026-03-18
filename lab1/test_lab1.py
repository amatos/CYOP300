"""
Author: Alberth Matos
CYOP300
Date:
Description:
"""

import pytest

import lab1_main as lab1
from lab1_main import InputError


def main():
    """Run all tests in this file."""
    raise SystemExit(pytest.main([__file__]))




def test_get_state_name_valid_abbreviation():
    """
    Tests the function get_state_name for valid state abbreviations.

    This test checks if the function correctly returns the full name of the
    state given a valid state abbreviation.

    Raises:
        AssertionError: If the state name returned does not match the
        expected output.
    """
    assert lab1.get_state_name("CA") == "California"


def test_get_state_name_invalid_abbreviation():
    """
    Tests the `get_state_name` function for handling invalid state abbreviations.

    This function ensures that an exception is raised when an unrecognized
    state abbreviation is provided to the `get_state_name` function. It evaluates
    the correctness of the error message and verifies that the appropriate
    custom exception is triggered.

    Raises:
        AssertionError: If the function does not raise the expected InputError
        exception or if the error message does not match the expected output.
    """
    with pytest.raises(InputError) as ex:
        lab1.get_state_name("XX")
    assert "not a recognised US state abbreviation" in str(ex.value)


def test_get_state_name_non_string_input():
    """
    Tests the behavior of the `get_state_name` function when a non-string input is provided.

    Raises:
        InputError: If the input to the `get_state_name` function is not of type string.
    """
    with pytest.raises(InputError) as ex:
        # noinspection PyTypeChecker
        lab1.get_state_name(123)
    assert "Expected a string" in str(ex.value)


def test_get_state_name_invalid_length():
    """
    Tests the behavior of the `get_state_name` function when given an invalid input length.

    This test ensures that the function correctly raises an `InputError` when the
    provided state abbreviation has a length other than exactly 2 characters.

    Raises:
        InputError: Raised when the state abbreviation is not 2 characters long.
    """
    with pytest.raises(InputError) as ex:
        lab1.get_state_name("ABC")
    assert "Abbreviation must be exactly 2 characters" in str(ex.value)


def test_get_age_valid(monkeypatch):
    """
    Test the get_age function with valid input.

    This test checks whether the get_age function correctly handles a valid age
    input and returns the expected integer value.

    Args:
        monkeypatch: pytest fixture used to replace the input function with
        a mock implementation that simulates user input.

    Raises:
        AssertionError: If the actual return value of get_age does not match
        the expected value.
    """
    monkeypatch.setattr("builtins.input", lambda: "25")
    assert lab1.get_age() == 25


def test_get_age_underage_returns_false(monkeypatch):
    """
    Tests the `get_age` function to ensure that it correctly returns False when the input age
    is below the legal threshold.

    Parameters:
    monkeypatch (MonkeyPatch): A pytest fixture used to dynamically replace the
        behavior of the `input` function for testing purposes.

    Raises:
    AssertionError: If the function does not return False when the input age is 17.
    """
    monkeypatch.setattr("builtins.input", lambda: "17")
    assert lab1.get_age() is False


def test_get_age_over_max_returns_false(monkeypatch):
    """
    Test function for verifying `get_age` behavior when age exceeds the maximum allowed value.

    Parameters:
    monkeypatch : pytest.MonkeyPatch
        Used to override the behavior of the built-in `input` function.

    Raises:
    AssertionError
        If the function does not return False for an input age exceeding
        the maximum threshold.
    """
    monkeypatch.setattr("builtins.input", lambda: "121")
    assert lab1.get_age() is False


def test_get_age_non_numeric_raises_input_error(monkeypatch):
    """
    Test function to verify that providing non-numeric input to the `get_age` function
    raises an `InputError`.

    This test uses the `monkeypatch` fixture to override the built-in `input` function
    with a lambda that returns a non-numeric string ("abc"). It then ensures that the
    `get_age` function raises an `InputError` and validates that the exception message
    contains the expected error text.

    Parameters:
        monkeypatch: pytest.MonkeyPatch
            A pytest fixture used to modify or patch the behavior of objects.

    Raises:
        InputError: Raised when `get_age` is provided non-numeric input for the year.
    """
    monkeypatch.setattr("builtins.input", lambda: "abc")
    with pytest.raises(InputError) as ex:
        lab1.get_age()
    assert "Please only enter digits for the year." in str(ex.value)


def test_get_age_100_or_more_confirm_yes(monkeypatch):
    """
    Tests the `get_age` function for the scenario where the entered age
    is exactly 100, and the user confirms the input with "Y".

    Parameters:
    monkeypatch (MonkeyPatch): A pytest fixture used for dynamically replacing
                               attributes during testing.

    Raises:
    AssertionError: If the function output does not match the expected result.
    """
    inputs = iter(["100", "Y"])
    monkeypatch.setattr("builtins.input", lambda: next(inputs))
    assert lab1.get_age() == 100


def test_get_age_100_or_more_confirm_no_then_reenter(monkeypatch):
    """
    Tests the functionality of the get_age method in `lab1` by simulating user input
    and verifying its correct behavior when provided with specific inputs.

    This test first provides a value of 100, simulating the user declining confirmation
    by entering "N", then re-enters a different valid value (25) for verification.

    Parameters:
        monkeypatch: A testing utility for modifying and simulating input/output during
        test execution.

    Returns:
        None
    """
    inputs = iter(["100", "N", "25"])
    monkeypatch.setattr("builtins.input", lambda: next(inputs))
    assert lab1.get_age() == 25


def test_get_age_100_or_more_confirm_quit(monkeypatch):
    """
    Tests the `get_age` function from the `lab1` module to ensure proper behavior
    when the user inputs an age of 100 or more and then chooses to quit. This test
    uses the `monkeypatch` fixture to mock user input.

    Args:
        monkeypatch: pytest fixture used to override `input` function behavior.

    Raises:
        AssertionError: If the function does not return the expected value.
    """
    inputs = iter(["100", "Q"])
    monkeypatch.setattr("builtins.input", lambda: next(inputs))
    assert lab1.get_age() is False


def test_get_state_valid(monkeypatch):
    """
    Tests the functionality of the `get_state` function with a valid state abbreviation.

    This test verifies that the `get_state` function correctly retrieves the full name
    and abbreviation of a state when a valid input abbreviation is provided via monkeypatching
    the built-in `input` function.

    Parameters:
    monkeypatch : MonkeyPatch
        A pytest fixture used to modify or replace parts of the code during testing.

    Returns:
    None
    """
    monkeypatch.setattr("builtins.input", lambda: "ca")
    assert lab1.get_state() == ("CA", "California")


def test_get_state_invalid_abbreviation_raises(monkeypatch):
    """
    Tests the behavior of the `get_state` function when an invalid state abbreviation is provided.

    This test replaces the standard input with a mocked input of "xx" (an invalid abbreviation)
    and checks if the `InputError` exception is raised as expected.

    Args:
        monkeypatch: A pytest fixture used to temporarily modify or mock objects, such as
            replacing built-in functions or inputs during the test.

    Raises:
        InputError: If the `get_state` function is called with an invalid abbreviation.
    """
    monkeypatch.setattr("builtins.input", lambda: "xx")
    with pytest.raises(InputError):
        lab1.get_state()


def test_get_country_of_citizenship_valid_simple(monkeypatch):
    """
    Tests the validity of the `get_country_of_citizenship` function when a simple, valid
    input is provided.

    Args:
        monkeypatch: pytest fixture used to patch built-in functions or objects for test purposes.
    """
    monkeypatch.setattr("builtins.input", lambda: "canada")
    assert lab1.get_country_of_citizenship() == "CANADA"


def test_get_country_of_citizenship_maps_usa_to_united_states(monkeypatch):
    """
    Tests the mapping of an input country abbreviation "usa" to its full form
    "UNITED STATES". This test checks the functionality of the
    lab1.get_country_of_citizenship function with the input being mocked.

    Parameters:
        monkeypatch: pytest.MonkeyPatch
            A pytest utility for dynamically altering and monkey-patching
            test behavior. It is used here to replace the input function.

    Returns:
        None

    Raises:
        AssertionError: If the output of lab1.get_country_of_citizenship does not match
        the expected value "UNITED STATES".
    """
    monkeypatch.setattr("builtins.input", lambda: "usa")
    assert lab1.get_country_of_citizenship() == "UNITED STATES"


def test_get_country_of_citizenship_reprompts_for_america(monkeypatch):
    """
    Tests the `get_country_of_citizenship` function to ensure it correctly handles
    re-prompting for input when "america" is initially entered and resolves it to
    "united states of america". It mocks input behavior to simulate user responses
    and verifies the function's expected output.

    Args:
        monkeypatch: pytest fixture used to patch built-in functions or objects
                     during tests. Here, it is used to mock user input.

    Raises:
        AssertionError: If the output of `get_country_of_citizenship` does not
        match the expected result.
    """
    inputs = iter(["america", "united states of america"])
    monkeypatch.setattr("builtins.input", lambda: next(inputs))
    assert lab1.get_country_of_citizenship() == "UNITED STATES OF AMERICA"


def test_get_country_of_citizenship_reprompts_for_invalid_characters(monkeypatch):
    """
    Tests the behavior of the `get_country_of_citizenship` function when invalid characters
    are entered initially, and valid input is entered subsequently.

    Parameters
    ----------
    monkeypatch : pytest.MonkeyPatch
        A pytest fixture to mock built-in function calls.

    Raises
    ------
    AssertionError
        If the function does not correctly prompt again for input or fails to return
        the expected processed output when provided valid input.
    """
    inputs = iter(["mexico1", "mexico"])
    monkeypatch.setattr("builtins.input", lambda: next(inputs))
    assert lab1.get_country_of_citizenship() == "MEXICO"


def test_get_name(monkeypatch):
    """
    Tests the `get_name` function from the `lab1` module.

    This test verifies that the `get_name` function correctly returns a tuple
    containing first and last names as provided by the `input` function. The
    `monkeypatch` fixture is used to simulate user input.

    Args:
        monkeypatch: pytest's monkeypatch fixture used for replacing or modifying
            the behavior of built-in functions or objects during tests.
    """
    inputs = iter(["Jane", "Doe"])
    monkeypatch.setattr("builtins.input", lambda: next(inputs))
    assert lab1.get_name() == ("Jane", "Doe")


def test_get_zipcode_valid_five_digit(monkeypatch):
    """
    Tests the 'get_zipcode' function for a valid five-digit ZIP code input.

    This test ensures that the function correctly processes and returns a
    valid five-digit ZIP code input provided through mocked user input.

    Parameters:
        monkeypatch (MonkeyPatch): A pytest fixture used to temporarily
        modify or replace functions, attributes, or objects for testing.

    Returns:
        None
    """
    monkeypatch.setattr("builtins.input", lambda: "12345")
    assert lab1.get_zipcode() == "12345"


def test_get_zipcode_valid_zip_plus_four_dash(monkeypatch):
    """
    Tests the `get_zipcode` function to ensure it correctly validates and
    retrieves a valid ZIP+4 code formatted with a dash.

    Attributes:
        monkeypatch: A pytest fixture used to temporarily modify or mock
        the behavior of objects or functions during the execution of the test.

    Parameters:
        monkeypatch: pytest.MonkeyPatch
            The pytest fixture to patch the input function for the test.

    Raises:
        AssertionError: If the `get_zipcode` function does not return the
            expected ZIP+4 code in the valid "12345-6789" format.
    """
    monkeypatch.setattr("builtins.input", lambda: "12345-6789")
    assert lab1.get_zipcode() == "12345-6789"


def test_get_zipcode_invalid_plus_then_valid(monkeypatch):
    """
    Tests the behavior of the get_zipcode function when provided with invalid
    and then valid ZIP code inputs.

    This test simulates user input by patching the built-in input function to
    return predefined ZIP code values. The first input simulates an invalid
    ZIP code format, while the second input provides a valid ZIP code format.
    It then verifies that the get_zipcode function correctly accepts the valid
    ZIP code and returns it.

    Args:
        monkeypatch: pytest fixture used to replace the built-in input function
        with a custom implementation for testing.

    Raises:
        AssertionError: If the get_zipcode function does not return the expected
        valid ZIP code.
    """
    inputs = iter(["12345+6789", "12345-6789"])
    monkeypatch.setattr("builtins.input", lambda: next(inputs))
    assert lab1.get_zipcode() == "12345-6789"


def test_get_zipcode_invalid_then_valid(monkeypatch):
    """
    Tests the behavior of the `get_zipcode` function with invalid and valid inputs.

    Summary:
    This test simulates the user entering an invalid input followed by a valid
    input for the `get_zipcode` function. It ensures that the function correctly
    handles the invalid input and then successfully accepts and returns the valid
    zipcode.

    Args:
    monkeypatch (pytest.MonkeyPatch): A pytest fixture used to replace or modify
    functions or objects during testing.

    Raises:
    AssertionError: If the assertion that the function returns the expected
    valid zipcode after handling the invalid input fails.
    """
    inputs = iter(["12", "12345"])
    monkeypatch.setattr("builtins.input", lambda: next(inputs))
    assert lab1.get_zipcode() == "12345"


def test_get_zipcode_quit_raises_system_exit(monkeypatch):
    """
    Test function for verifying that the get_zipcode function raises a SystemExit
    when the user chooses to quit by entering "q". The mocked user input is provided
    through monkeypatching.

    Args:
        monkeypatch: A pytest fixture that allows temporary modification
            of attributes or dictionaries for the scope of a test.

    Raises:
        SystemExit: Ensures the function terminates the program execution
            with a "Quitting..." message when "q" is entered as input.
    """
    monkeypatch.setattr("builtins.input", lambda: "q")
    with pytest.raises(SystemExit) as ex:
        lab1.get_zipcode()
    assert "Quitting..." in str(ex.value)


def test_main_user_not_old_enough(monkeypatch, capsys):
    """
    Tests the main function behavior when the user is not old enough to vote.

    This function simulates a scenario where the user's input age is below the voting
    eligibility threshold and verifies the corresponding output.

    Parameters:
    monkeypatch: pytest.MonkeyPatch
        Used for modifying the 'input' function to simulate user input.
    capsys: pytest.CaptureFixture
        Provides utilities to capture standard output and error during the test execution.
    """
    monkeypatch.setattr("builtins.input", lambda: "17")
    lab1.main()
    captured = capsys.readouterr()
    assert "not yet old enough to vote" in captured.out


def test_main_non_us_citizen(monkeypatch, capsys):
    """
    Tests the functionality of the `main` function for a non-US citizen scenario.

    This test simulates user input for age and citizenship to verify that the output
    correctly identifies when the user is not a US citizen.

    Attributes:
        monkeypatch: pytest fixture used to replace attributes and control inputs during testing.
        capsys: pytest fixture used to capture standard output during the test.

    Parameters:
        monkeypatch (pytest.MonkeyPatch): Fixture to modify the behavior of objects during testing.
        capsys (pytest.CaptureFixture): Fixture to capture printed output.

    Assertions:
        Verifies that the output string contains the phrase "not a US citizen" when the inputs
        provided involve a non-US citizen scenario.
    """
    inputs = iter(["25", "Canada"])
    monkeypatch.setattr("builtins.input", lambda: next(inputs))
    lab1.main()
    captured = capsys.readouterr()
    assert "not a US citizen" in captured.out


def test_main_eligible_and_registers(monkeypatch, capsys):
    """
    Tests the main function's behavior when the user is eligible to vote and completes the
    registration process.

    The test uses input mocking and output capturing to verify that the function handles
    correct input flow, determines eligibility to vote, and accurately processes and displays
    voter registration details.

    Parameters:
        monkeypatch (pytest.MonkeyPatch): A pytest fixture used to temporarily modify
            or mock built-in functions and objects.
        capsys (pytest.CaptureFixture): A pytest fixture to capture and inspect
            stdout and stderr output during the test execution.

    Raises:
        AssertionError: If the test validation fails for any expected part of the output.
    """
    inputs = iter([
        "25",
        "United States",
        "Jane",
        "Doe",
        "CA",
        "12345",
        "Y",
    ])
    monkeypatch.setattr("builtins.input", lambda: next(inputs))
    lab1.main()
    captured = capsys.readouterr()
    assert "eligible to vote" in captured.out
    assert "Your voter registration is as follows:" in captured.out
    assert "Name: Jane Doe" in captured.out
    assert "State of residency: California (CA)" in captured.out
    assert "Zipcode: 12345" in captured.out


def test_main_eligible_but_declines_registration(monkeypatch, capsys):
    """
    Tests the main function when the user is eligible to vote but declines registration.

    This function simulates user inputs to verify the behavior of the `main` function, ensuring
    that the program correctly identifies the voter as eligible and acknowledges their decision
    not to register.

    Parameters:
        monkeypatch (pytest.MonkeyPatch): A pytest fixture used to modify or replace
            attributes during testing, particularly to mock `input`.
        capsys (pytest.CaptureFixture): A pytest fixture to capture output streams
            during test execution.

    Assertions:
        Asserts that the output contains the expected text indicating the user is
        eligible to vote.
        Asserts that the output contains the expected text acknowledging the
        user's decision to decline registration.
    """
    inputs = iter([
        "25",
        "US",
        "John",
        "Smith",
        "NY",
        "10001",
        "N",
    ])
    monkeypatch.setattr("builtins.input", lambda: next(inputs))
    lab1.main()
    captured = capsys.readouterr()
    assert "eligible to vote" in captured.out
    assert "have not been registered to vote" in captured.out


def test_main_eligible_invalid_registration_response(monkeypatch, capsys):
    """
    Tests the behavior of the main function when encountering invalid input during
    the registration response stage.

    This test case ensures that the program appropriately handles an invalid
    registration response provided by the user by displaying a relevant error
    message.

    Parameters:
        monkeypatch: A pytest fixture used to modify or simulate the behavior of
        built-in functions, such as input(), within the test environment.
        capsys: A pytest fixture is used to capture standard output and standard
        error streams during the test execution.

    Assertions:
        Checks whether the output contains the error message "Invalid input.
        Please enter y or n." when an invalid registration response is provided.
    """
    inputs = iter([
        "25",
        "United States",
        "Alex",
        "Taylor",
        "TX",
        "75001",
        "MAYBE",
    ])
    monkeypatch.setattr("builtins.input", lambda: next(inputs))
    lab1.main()
    captured = capsys.readouterr()
    assert "Invalid input.  Please enter y or n." in captured.out


if __name__ == "__main__":
    main()
