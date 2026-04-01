import builtins
import pytest

import lab3.lab3common as common


def test_get_input_returns_converted_value(monkeypatch):
    monkeypatch.setattr(builtins, "input", lambda _: "42")
    assert common.get_input(int, "prompt") == 42


def test_get_input_retries_on_value_error(monkeypatch, capsys):
    answers = iter(["bad", "7"])
    monkeypatch.setattr(builtins, "input", lambda _: next(answers))
    assert common.get_input(int, "prompt") == 7
    assert "Invalid input" in capsys.readouterr().out


def test_get_yes_no_input_validates(monkeypatch):
    answers = iter(["maybe", "Y"])
    monkeypatch.setattr(common, "get_input", lambda _type, _prompt: next(answers))
    assert common.get_yes_no_input("prompt") == "y"


def test_exit_program_exits(capsys):
    with pytest.raises(SystemExit) as exc:
        common.exit_program()
    assert exc.value.code == 0
    assert "Exiting program" in capsys.readouterr().out


def test_rerun_or_return_uses_prompt_menu(monkeypatch):
    monkeypatch.setattr(common.Prompt, "indexed_menu", staticmethod(lambda options: 2))
    assert common.rerun_or_return() == 2
