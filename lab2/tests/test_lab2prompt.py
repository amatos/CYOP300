import pytest

from lab2 import lab2prompt


def test_menu_returns_selected_option(monkeypatch):
    class DummyMenu:
        def __init__(self, options):
            self.options = options

        def show(self):
            return 1

    monkeypatch.setattr(lab2prompt, "TerminalMenu", DummyMenu)

    result = lab2prompt.Prompt.menu(["first", "second", "third"])

    assert result == "second"


def test_menu_passes_options_to_terminal_menu(monkeypatch):
    captured = {}

    class DummyMenu:
        def __init__(self, options):
            captured["options"] = options

        def show(self):
            return 0

    monkeypatch.setattr(lab2prompt, "TerminalMenu", DummyMenu)

    result = lab2prompt.Prompt.menu(["alpha", "beta"])

    assert captured["options"] == ["alpha", "beta"]
    assert result == "alpha"


def test_dict_menu_calls_selected_function(monkeypatch):
    called = {"value": False}

    def action():
        called["value"] = True

    monkeypatch.setattr(
        lab2prompt.Prompt, "menu", staticmethod(lambda options: "Run it")
    )

    lab2prompt.Prompt.dict_menu({"Run it": action})

    assert called["value"] is True


def test_dict_menu_uses_dictionary_keys_in_order(monkeypatch):
    captured = {}

    def fake_menu(options):
        captured["options"] = options
        return "B"

    monkeypatch.setattr(lab2prompt.Prompt, "menu", staticmethod(fake_menu))

    called = {"a": False, "b": False}

    def action_a():
        called["a"] = True

    def action_b():
        called["b"] = True

    lab2prompt.Prompt.dict_menu({"A": action_a, "B": action_b})

    assert captured["options"] == ["A", "B"]
    assert called["b"] is True
    assert called["a"] is False
