from unittest.mock import patch

import admin
import pytest


def test_create_user_requires_name():
    message = admin.create_user(
        name="   ",
        username="user@example.com",
        password="ValidPassword1!",
    )

    assert message == "Name is required when creating a user."


def test_create_user_rejects_invalid_name():
    message = admin.create_user(
        name="Bad123",
        username="user@example.com",
        password="ValidPassword1!",
    )

    assert (
        message
        == "Invalid name format. Only alphabetic characters, spaces, hyphens, and apostrophes are allowed."
    )


def test_create_user_requires_username():
    message = admin.create_user(
        name="Valid Name",
        username="   ",
        password="ValidPassword1!",
    )

    assert message == "Username (e-mail address) is required when creating a user."


def test_create_user_rejects_invalid_email():
    message = admin.create_user(
        name="Valid Name",
        username="not-an-email",
        password="ValidPassword1!",
    )

    assert message == "Invalid email format. Please provide a valid email address."


def test_create_user_requires_password():
    message = admin.create_user(
        name="Valid Name",
        username="user@example.com",
        password=None,
    )

    assert message == "Password is required when creating a user."


def test_create_user_rejects_weak_password():
    message = admin.create_user(
        name="Valid Name",
        username="user@example.com",
        password="weak",
    )

    assert message == "Password does not meet requirements."


@patch("admin.db.create_user")
def test_create_user_returns_success_message(mock_create_user):
    mock_create_user.return_value = (True, "")

    message = admin.create_user(
        name=" Valid Name ",
        username=" user@example.com ",
        password="ValidPassword1!",
    )

    assert message == "User 'user@example.com' created."
    mock_create_user.assert_called_once_with(
        "Valid Name",
        "user@example.com",
        "ValidPassword1!",
    )


@patch("admin.db.create_user")
def test_create_user_returns_database_error_message(mock_create_user):
    mock_create_user.return_value = (False, "duplicate user")

    message = admin.create_user(
        name="Valid Name",
        username="user@example.com",
        password="ValidPassword1!",
    )

    assert message == "Error: User 'user@example.com' was not created: duplicate user"


def test_delete_user_requires_logged_in_session_user():
    message = admin.delete_user(
        username="user@example.com",
        session_username=None,
    )

    assert message == "You must be logged in to delete a user."


def test_delete_user_requires_username():
    message = admin.delete_user(
        username="   ",
        session_username="admin",
    )

    assert message == "A username is required."


def test_delete_user_prevents_self_deletion():
    message = admin.delete_user(
        username="admin@example.com",
        session_username="admin@example.com",
    )

    assert message == "You cannot delete yourself."


def test_delete_user_prevents_main_admin_deletion():
    message = admin.delete_user(
        username="admin",
        session_username="other-admin@example.com",
    )

    assert message == "You cannot delete the main admin user."


@patch("admin.db.delete_user")
def test_delete_user_returns_success_message(mock_delete_user):
    mock_delete_user.return_value = (True, "database success")

    message = admin.delete_user(
        username="user@example.com",
        session_username="admin@example.com",
    )

    assert message == "User 'user@example.com' deleted."
    mock_delete_user.assert_called_once_with("user@example.com")


@patch("admin.db.delete_user")
def test_delete_user_returns_database_failure_message(mock_delete_user):
    mock_delete_user.return_value = (False, "user not found")

    message = admin.delete_user(
        username="missing@example.com",
        session_username="admin@example.com",
    )

    assert message == "user not found"


def test_change_password_requires_username():
    message = admin.change_password(
        username="   ",
        password="ValidPassword1!",
    )

    assert message == "A username is required."


def test_change_password_requires_password():
    message = admin.change_password(
        username="user@example.com",
        password="   ",
    )

    assert message == "A new password is required."


def test_change_password_rejects_weak_password():
    message = admin.change_password(
        username="user@example.com",
        password="weak",
    )

    assert message == "Password does not meet requirements."


@patch("admin.db.change_password")
def test_change_password_returns_success_message(mock_change_password):
    mock_change_password.return_value = (True, "database success")

    message = admin.change_password(
        username=" user@example.com ",
        password="ValidPassword1!",
    )

    assert message == "Password changed for user 'user@example.com'."
    mock_change_password.assert_called_once_with("user@example.com", "ValidPassword1!")


@patch("admin.db.change_password")
def test_change_password_returns_database_failure_message(mock_change_password):
    mock_change_password.return_value = (False, "user not found")

    message = admin.change_password(
        username="missing@example.com",
        password="ValidPassword1!",
    )

    assert message == "user not found"
