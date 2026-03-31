import pytest

import lab3.lab3common


def test_get_input_valid(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda prompt="": "42")
    assert lab3.lab3common.get_input(int, "Enter a number: ") == 42


def test_get_input_retries_on_invalid(monkeypatch, capsys):
    responses = iter(["abc", "7"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(responses))

    result = lab3.lab3common.get_input(int, "Enter a number: ")

    assert result == 7
    out = capsys.readouterr().out
    assert "Invalid input" in out


def test_get_yes_no_input_accepts_y(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda prompt="": "Y")
    assert lab3.lab3common.get_yes_no_input("Continue? ") == "y"


def test_get_yes_no_input_retries_until_valid(monkeypatch, capsys):
    responses = iter(["maybe", "n"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(responses))

    result = lab3.lab3common.get_yes_no_input("Continue? ")

    assert result == "n"
    out = capsys.readouterr().out
    assert "Invalid input" in out


def test_exit_program_raises_system_exit(capsys):
    with pytest.raises(SystemExit) as excinfo:
        lab3.lab3common.exit_program()

    assert excinfo.value.code == 0
    out = capsys.readouterr().out
    assert "Exiting program" in out
