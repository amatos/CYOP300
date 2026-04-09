"""
Author: Alberth Matos
CYOP300
Date: 07 April 2026
Description:
"""

import hashlib


def main() -> None:
    """
    Hashlib usage example, as provided by the Lab4 documentation.

    :return: None
    :rtype: None
    """
    # input a message to encode
    print("Enter a message to encode:")
    message = input()
    # encode it to bytes using UTF-8 encoding
    message = message.encode()
    # hash with MD5 (very weak)
    print(hashlib.md5(message).hexdigest())
    # Lets try a stronger SHA-2 family
    print(hashlib.sha256(message).hexdigest())
    print(hashlib.sha512(message).hexdigest())


if __name__ == "__main__":
    main()
