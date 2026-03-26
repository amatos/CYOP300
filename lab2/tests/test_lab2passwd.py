import random
import secrets
import string

import pytest

from lab2 import lab2passwd


def test_build_password_requirements_happy_path(monkeypatch):
    responses = iter([8, "y", "n", "y", "n"])

    monkeypatch.setattr(
        lab2passwd.lab2common, "get_input", lambda _type, prompt: next(responses)
    )
    monkeypatch.setattr(
        lab2passwd.lab2common, "get_yes_no_input", lambda prompt: next(responses)
    )

    length, required_counts, allowed = lab2passwd.build_password_requirements()

    assert length == 8
    assert required_counts == {"upper": 1, "lower": 0, "digits": 1, "special": 0}
    assert all(ch in (string.ascii_uppercase + string.digits) for ch in allowed)


def test_build_password_requirements_raises_when_too_short(monkeypatch):
    responses = iter([1, "y", "y", "n", "n"])

    monkeypatch.setattr(
        lab2passwd.lab2common, "get_input", lambda _type, prompt: next(responses)
    )
    monkeypatch.setattr(
        lab2passwd.lab2common, "get_yes_no_input", lambda prompt: next(responses)
    )

    with pytest.raises(ValueError, match="Password length is too short"):
        lab2passwd.build_password_requirements()


def test_count_character_types_counts_all_categories():
    password = "Ab3!"
    counts = lab2passwd.count_character_types(password)

    assert counts == {"upper": 1, "lower": 1, "digits": 1, "special": 1}


def test_generate_password_includes_required_types_and_length(monkeypatch):
    choices = iter(["A", "b", "3", "!", "x", "Y"])
    shuffled = []

    monkeypatch.setattr(secrets, "choice", lambda pool: next(choices))
    monkeypatch.setattr(
        random, "shuffle", lambda items: shuffled.extend(items) or items.reverse()
    )

    password = lab2passwd.generate_password(
        6,
        {"upper": 1, "lower": 1, "digits": 1, "special": 1},
        string.ascii_uppercase
        + string.ascii_lowercase
        + string.digits
        + string.punctuation,
    )

    assert len(password) == 6
    assert set("Ab3!") <= set(password)
    assert shuffled  # proves shuffle was reached
