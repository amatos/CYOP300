import hashlib

import pytest
import toolbox


@pytest.mark.parametrize(
    "name",
    [
        "Alice",
        "Alice Smith",
        "Anne-Marie Smith",
        "O'Connor",
        "Smith, John",
    ],
)
def test_is_valid_name_accepts_safe_names(name):
    assert toolbox.is_valid_name(name) is True


@pytest.mark.parametrize(
    "name",
    [
        "",
        "   ",
        "Alice123",
        "Robert; DROP TABLE users;",
        "<script>alert(1)</script>",
        "Alice_Example",
    ],
)
def test_is_valid_name_rejects_invalid_names(name):
    assert toolbox.is_valid_name(name) is False


@pytest.mark.parametrize(
    "email",
    [
        "user@example.com",
        "first.last@example.co.uk",
        "user+tag@example.org",
        "user_name@example-domain.com",
    ],
)
def test_is_valid_email_accepts_valid_email_format(email):
    assert toolbox.is_valid_email(email) is True


@pytest.mark.parametrize(
    "email",
    [
        "",
        "plainaddress",
        "missing-at.example.com",
        "missing-domain@",
        "@missing-user.com",
        "user@example",
        "user@example.",
        "user name@example.com",
        "user@example.com;DROP TABLE users;",
    ],
)
def test_is_valid_email_rejects_invalid_email_format(email):
    assert toolbox.is_valid_email(email) is False


@pytest.mark.parametrize(
    "password",
    [
        "ValidPassword1!",
        "Another-Good-Password9",
        "LongEnoughWithNumber7#",
    ],
)
def test_validate_password_accepts_valid_passwords(password):
    assert toolbox.validate_password(password) is True


@pytest.mark.parametrize(
    "password",
    [
        "",
        "short1!",
        "alllowercasepassword1!",
        "ALLUPPERCASEPASSWORD1!",
        "NoNumberPassword!",
        "NoSpecialPassword1",
    ],
)
def test_validate_password_rejects_invalid_passwords(password):
    assert toolbox.validate_password(password) is False


def test_hash_password_returns_sha256_hex_digest():
    password = "ValidPassword1!"
    expected_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()

    assert toolbox.hash_password(password) == expected_hash


def test_hash_password_same_input_returns_same_hash():
    password = "ValidPassword1!"

    assert toolbox.hash_password(password) == toolbox.hash_password(password)


def test_hash_password_different_inputs_return_different_hashes():
    assert toolbox.hash_password("ValidPassword1!") != toolbox.hash_password(
        "DifferentPassword1!"
    )
