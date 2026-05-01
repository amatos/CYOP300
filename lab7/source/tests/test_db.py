import sqlite3
from pathlib import Path

import db
import pytest
from toolbox import hash_password


@pytest.fixture
def temp_database(tmp_path, monkeypatch):
    database_path = tmp_path / "accounts.db"
    monkeypatch.setattr(db, "DATABASE_PATH", database_path)

    with sqlite3.connect(database_path) as conn:
        conn.execute("""
            CREATE TABLE roles (
                                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                                   role TEXT NOT NULL UNIQUE
            )
            """)
        conn.execute("""
            CREATE TABLE users (
                                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                                   name TEXT,
                                   username TEXT NOT NULL UNIQUE,
                                   password TEXT NOT NULL,
                                   role_id INTEGER NOT NULL REFERENCES roles(id)
            )
            """)
        conn.execute("INSERT INTO roles (id, role) VALUES (1, 'admin')")
        conn.execute("INSERT INTO roles (id, role) VALUES (2, 'user')")
        conn.execute(
            """
            INSERT INTO users (name, username, password, role_id)
            VALUES (?, ?, ?, ?)
            """,
            ("Admin User", "admin", hash_password("AdminPassword1!"), 1),
        )
        conn.execute(
            """
            INSERT INTO users (name, username, password, role_id)
            VALUES (?, ?, ?, ?)
            """,
            ("Regular User", "user@example.com", hash_password("UserPassword1!"), 2),
        )

    return database_path


def test_execute_db_write_returns_affected_row_count(temp_database):
    rowcount = db.execute_db_write(
        "UPDATE users SET name = ? WHERE username = ?",
        ("Updated User", "user@example.com"),
    )

    assert rowcount == 1


def test_query_rowcount_result_handles_not_found():
    succeeded, message = db.query_rowcount_result(
        0,
        "not found",
        "success",
    )

    assert succeeded is False
    assert message == "not found"


def test_query_rowcount_result_handles_success():
    succeeded, message = db.query_rowcount_result(
        1,
        "not found",
        "success",
    )

    assert succeeded is True
    assert message == "success"


def test_query_rowcount_result_handles_duplicate_when_message_is_provided():
    succeeded, message = db.query_rowcount_result(
        2,
        "not found",
        "success",
        "duplicate",
    )

    assert succeeded is False
    assert message == "duplicate"


def test_get_users_returns_users_with_roles(temp_database):
    users, succeeded, message = db.get_users()

    assert succeeded is True
    assert message == ""
    assert ("Admin User", "admin", "admin") == (
        users[0][1],
        users[0][2],
        users[0][3],
    )


def test_create_user_inserts_valid_user(temp_database):
    succeeded, message = db.create_user(
        "New User",
        "new@example.com",
        "ValidPassword1!",
    )

    assert succeeded is True
    assert message == "User new@example.com created successfully."


def test_create_user_rejects_invalid_password(temp_database):
    succeeded, message = db.create_user(
        "New User",
        "new@example.com",
        "weak",
    )

    assert succeeded is False
    assert message == ""


def test_create_user_rejects_duplicate_username(temp_database):
    succeeded, message = db.create_user(
        "Duplicate User",
        "user@example.com",
        "ValidPassword1!",
    )

    assert succeeded is False
    assert message == "Username user@example.com already exists."


def test_authenticate_user_accepts_correct_password(temp_database):
    succeeded, message = db.authenticate_user("user@example.com", "UserPassword1!")

    assert succeeded is True
    assert message == "User user@example.com logged in successfully."


def test_authenticate_user_rejects_incorrect_password(temp_database):
    succeeded, message = db.authenticate_user("user@example.com", "WrongPassword1!")

    assert succeeded is False
    assert message == "User user@example.com unable to log in."


def test_user_is_admin_returns_true_for_admin_user(temp_database):
    assert db.user_is_admin("admin") is True


def test_user_is_admin_returns_false_for_regular_user(temp_database):
    assert db.user_is_admin("user@example.com") is False


def test_change_password_updates_existing_user(temp_database):
    succeeded, message = db.change_password("user@example.com", "NewPassword1!")

    assert succeeded is True
    assert message == "User user@example.com password updated successfully."

    authenticated, _ = db.authenticate_user("user@example.com", "NewPassword1!")
    assert authenticated is True


def test_change_password_raises_value_error_for_invalid_password(temp_database):
    with pytest.raises(
        ValueError, match="Password does not meet complexity requirements"
    ):
        db.change_password("user@example.com", "weak")


def test_change_password_returns_false_for_missing_user(temp_database):
    succeeded, message = db.change_password("missing@example.com", "NewPassword1!")

    assert succeeded is False
    assert (
        message
        == "Could not update user password: User missing@example.com does not exist."
    )


def test_delete_user_removes_existing_user(temp_database):
    succeeded, message = db.delete_user("user@example.com")

    assert succeeded is True
    assert message == "User user@example.com deleted successfully."

    authenticated, _ = db.authenticate_user("user@example.com", "UserPassword1!")
    assert authenticated is False


def test_delete_user_returns_false_for_missing_user(temp_database):
    succeeded, message = db.delete_user("missing@example.com")

    assert succeeded is False
    assert message == "Could not delete user: missing@example.com does not exist."
