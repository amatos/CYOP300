import builtins

import pytest

from lab2 import lab2common


def test_get_input_retries_until_valid(monkeypatch):
    inputs = iter(["bad", "42"])

    monkeypatch.setattr(builtins, "input", lambda prompt: next(inputs))

    result = lab2common.get_input(int, "Enter number: ")

    assert result == 42


def test_get_yes_no_input_accepts_uppercase(monkeypatch):
    inputs = iter(["maybe", "Y"])

    monkeypatch.setattr(lab2common, "get_input", lambda _type, prompt: next(inputs))

    result = lab2common.get_yes_no_input("Continue? ")

    assert result == "y"


def test_get_input_in_mm_converts_km_to_mm(monkeypatch):
    inputs = iter([2.5, "km"])

    monkeypatch.setattr(lab2common, "get_input", lambda _type, prompt: next(inputs))

    value, unit = lab2common.get_input_in_mm("length", "test object")

    assert value == 2500.0
    assert unit == "km"


def test_get_input_in_mm_retries_on_invalid_unit(monkeypatch):
    inputs = iter([3, "yards", 3, "cm"])

    monkeypatch.setattr(lab2common, "get_input", lambda _type, prompt: next(inputs))

    value, unit = lab2common.get_input_in_mm("width", "test object")

    assert value == pytest.approx(0.3)
    assert unit == "cm"
