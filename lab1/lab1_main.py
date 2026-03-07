"""
Author: Alberth Matos
CYOP300
Date:
Description: This module contains the main functionality of Lab1:
  - Prompt the user for their age
  - Prompt the user for their nationality
  - If they are at least 18 years of age, and a US citizen, as if they wish
    to register to vote. If so:
      - Prompt the user for their name
      - Prompt the user for their state of residency
      - Prompt the user for their zipcode
      - Offer to register the user to vote
"""

import re                   # the standard regex library
from lab1 import InputError # Input error class from the main module

def get_state_name(abbreviation: str) -> str:
    """
    Returns the full name of a US state given its two-character abbreviation.

    This function uses a predefined map of US state abbreviations to their
    corresponding full names. It validates the input to ensure that the provided
    abbreviation is a string of exactly two characters and corresponds to a valid
    US state.

    Parameters:
    abbreviation: str
        A two-character string representing the abbreviation of a US state.

    Raises:
    InputError
        If `abbreviation` is not a string.
        If `abbreviation` is not exactly two characters long.
        If `abbreviation` is not a valid US state abbreviation.

    Returns:
    str
        The full name of the US state corresponding to the given abbreviation.
    """

    # Map of US state abbreviations to their respective full names
    state_abbrev_map: dict[str, str] = {
        "AL": "Alabama",
        "AK": "Alaska",
        "AZ": "Arizona",
        "AR": "Arkansas",
        "CA": "California",
        "CO": "Colorado",
        "CT": "Connecticut",
        "DE": "Delaware",
        "FL": "Florida",
        "GA": "Georgia",
        "HI": "Hawaii",
        "ID": "Idaho",
        "IL": "Illinois",
        "IN": "Indiana",
        "IA": "Iowa",
        "KS": "Kansas",
        "KY": "Kentucky",
        "LA": "Louisiana",
        "ME": "Maine",
        "MD": "Maryland",
        "MA": "Massachusetts",
        "MI": "Michigan",
        "MN": "Minnesota",
        "MS": "Mississippi",
        "MO": "Missouri",
        "MT": "Montana",
        "NE": "Nebraska",
        "NV": "Nevada",
        "NH": "New Hampshire",
        "NJ": "New Jersey",
        "NM": "New Mexico",
        "NY": "New York",
        "NC": "North Carolina",
        "ND": "North Dakota",
        "OH": "Ohio",
        "OK": "Oklahoma",
        "OR": "Oregon",
        "PA": "Pennsylvania",
        "RI": "Rhode Island",
        "SC": "South Carolina",
        "SD": "South Dakota",
        "TN": "Tennessee",
        "TX": "Texas",
        "UT": "Utah",
        "VT": "Vermont",
        "VA": "Virginia",
        "WA": "Washington",
        "WV": "West Virginia",
        "WI": "Wisconsin",
        "WY": "Wyoming",
    }

    # If `abbreviation` is not a string, raise an exception.
    if not isinstance(abbreviation, str):
        raise InputError(
            f"Expected a string, got {type(abbreviation).__name__!r} instead."
        )

    # If `abbreviation` is not exactly two characters, raise an exception.
    if len(abbreviation) != 2:
        raise InputError("Abbreviation must be exactly 2 characters.")

    # If `abbreviation` is not a key in state_abbrev_map (that is, isn't a valid
    # US state abbreviation), raise an exception.
    if abbreviation not in state_abbrev_map:
        raise InputError(f"{abbreviation!r} is not a recognised US state "
                         f"abbreviation.")

    # Otherwise, return the name of the state corresponding to the abbreviation.
    # This serves as a check that the abbreviation maps to an actual state.
    return state_abbrev_map[abbreviation]


def get_age() -> int | bool:
    """
    Determines and validates the age of a user, ensuring the age entered is a
    reasonable value. If the entered age is above 100, an additional
    confirmation from the user is required. Returns the confirmed age if valid,
    or False if an invalid age or cancellation is detected.

    Raises:
        InputError: If the user inputs non-integer values when entering age.

    Returns:
        int | bool: The confirmed valid age as an integer if the user enters
        appropriate data, or False if the input is invalid or the user cancels
        the operation.
    """

    # Initialize variables
    confirmed_age = False   # Used in while loop to check if age is confirmed.
    age = False             # Return value.  int if the age is valid, False
                            # if an invalid age is provided.

    # Loop until a valid age entered (or confirmed if age > 100), of the user
    # enters q to quit.
    while not confirmed_age:
        print("What is your age?")
        # Try block to get user input and catch ValueError if non-integer input.
        try:
            age = int(input())
        except ValueError as ex:
            raise InputError("Please only enter digits for the year.") from ex
        # Check if age is within the voting range, higher than 100 (which may
        # be possible), or higher than 120, which is a reasonable value for
        # a human maximum.
        if age < 18:
            print("You are not yet old enough to vote.  Please return when "
                  "you are 18 years of age or older.")
            age = -1
            confirmed_age = True
        elif age > 120:
            print("Your age is above the known maximum age. Please contact "
                  "your local election official for more information.")
            age = -1
            confirmed_age = True
        elif age >= 100:
            # If the age is greater than or equal to 100 (but less than 121),
            # verify with the user that they have entered the correct date
            # using check_uncommon_age().
            check_age, new_age = check_uncommon_age(age)
            if check_age:
                age = new_age
                confirmed_age = True
        # If age is >= 18, or < 100, set confirmed_age to True to exit the
        # loop because no additional confirmation is needed.
        else:
            confirmed_age = True
    # If age is not -1, return age.  Otherwise, return False to indicate an
    # invalid age.
    if age != -1:
        return age
    return False

def check_uncommon_age(age: int) -> tuple[bool, int]:
    """
    If a user provides an age between 100 and 120 inclusive, verify with the
    user that they have entered the correct age.  If they have not, provide
    the user with an opportunity to re-enter their age, or to quit.

    Parameters:
    age (int): The age value to be confirmed by the user.

    Returns:
    tuple[bool, int]: A tuple containing:
        - A boolean indicating whether the age has been confirmed or rejected.
        - An integer representing the confirmed or updated age, or -1 if the
        user quits.
    """
    age_prompt = False  # Used in while loop in case we need to re-prompt
                        # for age.
    check = False       # Boolean value to indicate success or failure of age
                        # confirmation.
    confirmation = ""   # Used to store user input for confirmation of age.
                        # Should be Y, N, or Q.
    print("Your age is higher than usual. Please confirm that you "
          f"are {age} years old. Please enter Y for yes, N for no, "
          "or Q to quit.")
    # Loop until a valid confirmation is entered (Y, N, or Q).
    while not age_prompt:
        # Try block to get user input.  If non-string input is provided,
        # print a message requesting a valid input and continue the loop to
        # prompt again.
        try:
            print("Y/N/Q: ")
            confirmation = input().upper()
            if confirmation not in ("Y", "N", "Q"):
                print("Please enter y, n, or q.")
            else:
                age_prompt = True
        except ValueError:
            print("Please enter Y, N, or Q.")
    # Once out of the while loop, handle user input:
    #   - If N, prompt the user to re-enter their age and loop again.
    #   - If Y, set confirmed_age to True to exit the loop.
    #   - If Q, set age to -1, indicating an invalid age.
    if confirmation == "N":
        check = False
    if confirmation == "Y":
        check = True
    if confirmation == "Q":
        check = True
        age = -1
    # Return the tuple containing the confirmation status and age.
    return check, age

def get_state() -> tuple[str, str]:
    """
    Retrieve the state abbreviation and full state name based on user input.

    The function prompts the user to provide their state abbreviation,
    converting it to uppercase for consistency. It validates the input
    by using the `get_state_name()` function. If the abbreviation is
    invalid, an exception will be raised. Upon successful validation,
    the function returns the abbreviation and the full state name.

    Returns:
        tuple[str, str]: A tuple containing the state abbreviation and
        the full name of the state.
    """
    stateless = True
    state = ""
    abbreviation = ""

    while stateless:
        try:
            print("Please enter your state abbreviation (i.e. CA for California): ")
            # Prompt for input and convert it to upper-case.  get_state_name()
            # will handle validation and raise an exception if the
            # abbreviation is invalid.
            abbreviation = input().upper()
            state = get_state_name(abbreviation)
            if state != "":
                stateless = False
        except InputError:
            print(f"Invalid state abbreviation: {abbreviation!r}.")
            print("Please enter a valid state abbreviation.")

    # Return the abbreviation, as well as the full name of the state
    return abbreviation, state

def get_country_of_citizenship() -> str | None:
    """
    Prompts the user to input their country of citizenship and validates the
    input.

    This function repeatedly prompts the user until a valid country of
    citizenship is provided. The input is normalized to uppercase and checked
    against a regular expression to ensure it only contains alphabetical
    characters and spaces. Additionally, specific input values are
    interpreted to adjust or clarify responses. For example, input like "USA"
    or "U.S.A." is normalized to "United States". The function ensures
    accuracy by confirming ambiguous inputs, such as replacing "America" with
    the appropriate name.

    Returns:
        str | None: The validated and normalized country of citizenship
        entered by the user.
    """

    confirmed = False
    citizenship = None

    while not confirmed:
        print("Please enter your country of citizenship: ")
        citizenship = input().upper()
        if citizenship in ('USA', 'U.S.A.', 'U.S.'):
            citizenship = "United States".upper()
        while citizenship == "America".upper():
            print("Did you mean United States of America?  Please enter United "
                  "States of America, United States, USA, U.S.A., US, or U.S. "
                  "for your country of citizenship.")
            citizenship = input().upper()
        # The pattern explanation:
        # ^: Matches the start of the string.
        # [A-Z ]: Matches any character in the range A-Z (case-sensitive) or a
        #   space character.
        # +: Ensure that there are one or more occurrences of the allowed
        #   chars to prevent empty strings from matching.
        # $: Matches the end of the string.
        pattern = r"^[A-Z ]+$"
        if re.match(pattern, citizenship):
            confirmed = True
        else:
            print(f"Country names should include only alpha characters, and "
                  f"possibly a space.  You entered {citizenship}. Please enter "
                  f"a valid country of citizenship.")
    return citizenship

def get_name() -> tuple[str, str]:
    """
    Gets the first and last name as input from the user and returns them as a
    tuple.

    Returns:
        tuple[str, str]: A tuple where the first element is the first name and
        the second element is the last name.
    """
    print("Please enter your first name: ")
    first_name = input()
    print("Please enter your last name: ")
    last_name = input()
    return first_name, last_name


def get_zipcode() -> str:
    """
    Validates and retrieves a correctly formatted U.S. zipcode from user input.

    This function repeatedly prompts the user to enter a valid U.S. zipcode.
    It accepts either a 5-digit zipcode or a zip+4 code with a dash (e.g.,
    12345-6789). The prompt can be exited by entering 'q', which ends the
    program. The function ensures the input adheres to the correct format
    before returning it.

    Raises:
        SystemExit: If the user enters 'q' to quit the prompt.

    Returns:
        str: A valid U.S. zipcode entered by the user.
    """
    valid_zip = False
    zipcode = None
    pattern = r"^\d{5}(-\d{4})?$"

    while not valid_zip:
        print("Please enter your zipcode: ")
        print("please use either a 5-digit zipcode or zip+4 zipcode with "
              "a dash separating the group of 5 and 4, or q to quit:")
        zipcode = input()
        if re.fullmatch(pattern, zipcode):
            valid_zip = True
        else:
            if zipcode == "q":
                raise SystemExit("Quitting...")
            print("Invalid zipcode.  Please re-enter.")

    return zipcode

def main():
    """
    Determines voter eligibility and processes voter registration.

    Returns:
        None
    """
    can_vote = False
    citizenship = False
    country_of_citizenship = None

    print("*" * 80)
    print("Welcome to the voter registration program.")
    print("*" * 80)

    # Age must be greater than or equal to 18.
    age = get_age()
    # get_age() returns one of several values:
    #   - An integer value representing the age of the user, if the age is
    #     valid and confirmed (if necessary).
    #   - False, if the age is invalid
    # This check allows the program to continue if and only if the age is
    # valid.
    if age:
        country_of_citizenship = get_country_of_citizenship()
        # Since we only specifically care about citizens of the United States,
        # we allow two possible values for country_of_citizenship:
        #   - "UNITED STATES"
        #   - "US"
        # Since it is not uncommon for the entire formal country name to be
        # spelled out, in case the user provides "United States of America", we
        # only look at the first 13 characters of the string
        if ((country_of_citizenship[0:13] == "UNITED STATES") or
            (country_of_citizenship == "US")):
            citizenship = True

        # For the remaining questions, it only makes sense to ask the user for
        # input if, and only if, they are both a US citizen and 18 years of age.
        # If the user is a US citizen and is 18 years of age or older, set
        # the can_vote flag to True and print a congratulatory message.
        # Otherwise, print a message indicating that the user is not eligible
        # to vote.
        if citizenship and age:
            print("Congratulations!  As a US Citizen, 18 years of age or older, "
                  "you are eligible to vote.\n\n")
            can_vote = True
        elif not citizenship:
            print("Sorry, you are not a US citizen. You are not eligible to vote.\n")

    # If can_vote is true, prompt the user for their name, state of residency,
    # and zipcode.
    if can_vote:
        first_name, last_name = get_name()
        st, state = get_state() # The full state name is used in the dialogue,
                                # but the 2-character abbreviation is used for
                                # the mailing address
        zipcode = get_zipcode()

        print(f"Thank you, {first_name}. You are eligible to vote in {state}. Do "
              f"you want to register? (y/n)")
        answer = input().upper()
        # If the user indicates that they want to register, print out a
        # registration summary and state that their registration has been
        # submitted.
        # If the user indicates that they do not want to register, print
        # a message indicating that they have not been registered.
        if answer == "Y":
            print("\n" + "*"*80)
            print("Your voter registration is as follows:")
            print(f"Name: {first_name} {last_name}")
            print(f"Age: {age}")
            print(f"State of residency: {state} ({st})")
            print(f"Zipcode: {zipcode}")
            print(f"Country of citizenship: {country_of_citizenship}")
            print("\n\nYour voter registration has been submitted. You should "
                  "receive your voter registration card within 3 weeks.\n\n")
            print("*" * 80)
            print("The mailing label for your voter registration card is:")
            print(f"{first_name} {last_name}")
            print("123 main street")
            print(f"Anytown, {st} {zipcode}")
            print("*" * 80)

        elif answer == "N":
            print("*" * 80)
            print("Thank you!  You have not been registered to vote.")
            print("*" * 80)
        else:
            print("Invalid input.  Please enter y or n.")

if __name__ == "__main__":
    main()
