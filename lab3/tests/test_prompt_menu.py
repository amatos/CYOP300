from unittest.mock import Mock

import lab3.lab3prompt as prompt_mod


def test_prompt_menu_returns_selected_item(monkeypatch):
    class FakeMenu:
        def __init__(self, options):
            self.options = options

        def show(self):
            return 1

    monkeypatch.setattr(prompt_mod, "TerminalMenu", FakeMenu)
    assert prompt_mod.Prompt.menu(["a", "b", "c"]) == "b"


def test_prompt_dict_menu_executes_selected_function(monkeypatch):
    called = []

    monkeypatch.setattr(prompt_mod.Prompt, "menu", staticmethod(lambda options: "Run"))

    def run():
        called.append(True)

    prompt_mod.Prompt.dict_menu({"Run": run})
    assert called == [True]


def test_prompt_indexed_menu_returns_index(monkeypatch):
    class FakeMenu:
        def __init__(self, options):
            self.options = options

        def show(self):
            return 0

    monkeypatch.setattr(prompt_mod, "TerminalMenu", FakeMenu)
    assert prompt_mod.Prompt.indexed_menu(["x", "y"]) == 0
