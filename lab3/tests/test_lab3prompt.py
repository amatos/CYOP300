import lab3.lab3prompt


def test_prompt_menu_selects_option(monkeypatch):
    class FakeTerminalMenu:
        def __init__(self, options):
            self.options = options

        def show(self):
            return 1

    monkeypatch.setattr(lab3.lab3prompt, "TerminalMenu", FakeTerminalMenu)

    result = lab3.lab3prompt.Prompt.menu(["A", "B", "C"])

    assert result == "B"


def test_dict_menu_calls_selected_function(monkeypatch):
    monkeypatch.setattr(
        lab3.lab3prompt.Prompt, "menu", staticmethod(lambda options: "Hello")
    )

    called = {"value": False}

    def handler():
        called["value"] = True

    lab3.lab3prompt.Prompt.dict_menu({"Hello": handler})

    assert called["value"] is True
