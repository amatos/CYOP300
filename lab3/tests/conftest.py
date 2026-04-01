import builtins
import pytest

import lab3.lab3common as common
import lab3.lab3prompt as prompt_mod
import lab3.lab3states as states_mod
import lab3.lab3search_states as search_mod


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


@pytest.fixture
def dummy_states_data():
    return [
        {
            "state": "Alabama",
            "abbreviation": "AL",
            "capital": "Montgomery",
            "population": "1000",
            "flower": "Camellia",
        },
        {
            "state": "California",
            "abbreviation": "CA",
            "capital": "Sacramento",
            "population": "2000",
            "flower": "Poppy",
        },
        {
            "state": "Texas",
            "abbreviation": "TX",
            "capital": "Austin",
            "population": "3000",
            "flower": "Bluebonnet",
        },
        {
            "state": "Florida",
            "abbreviation": "FL",
            "capital": "Tallahassee",
            "population": "4000",
            "flower": "Orange Blossom",
        },
        {
            "state": "New York",
            "abbreviation": "NY",
            "capital": "Albany",
            "population": "5000",
            "flower": "Rose",
        },
        {
            "state": "Illinois",
            "abbreviation": "IL",
            "capital": "Springfield",
            "population": "6000",
            "flower": "Violet",
        },
    ]


@pytest.fixture
def dummy_state():
    return {
        "state": "Texas",
        "abbreviation": "TX",
        "capital": "Austin",
        "population": "3000",
        "flower": "Bluebonnet",
    }


class DummyStates:
    def __init__(self, state_data=None):
        self.state_data = state_data or []
        self.write_calls = []

    def __iter__(self):
        return iter(self.state_data)

    def get_state_by_abbreviation(self, abbrev):
        for state in self.state_data:
            if state["abbreviation"].lower() == abbrev.lower():
                return state
        return None

    def get_state_by_name(self, name):
        for state in self.state_data:
            if state["state"].lower() == name.lower():
                return state
        return None

    def write_state_data(self, data):
        self.write_calls.append(data)


@pytest.fixture
def dummy_states(dummy_states_data):
    return DummyStates(dummy_states_data)


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


def test_states_getters_and_update(monkeypatch):
    dummy = states_mod.States.__new__(states_mod.States)
    dummy.state_data = [
        {"state": "Texas", "abbreviation": "TX", "population": "3000"},
        {"state": "California", "abbreviation": "CA", "population": "2000"},
    ]
    monkeypatch.setattr(states_mod.States, "write_state_data", lambda self, data: None)

    assert states_mod.States.get_state_by_abbreviation(dummy, "tx")["state"] == "Texas"
    assert (
        states_mod.States.get_state_by_name(dummy, "california")["abbreviation"] == "CA"
    )
    assert states_mod.States.update_state_population(dummy, "Texas", 9999) is True
    assert dummy.state_data[0]["population"] == "9999"
    assert states_mod.States.update_state_population(dummy, "Nevada", 1) is False


def test_search_by_abbrev_returns_state(monkeypatch, dummy_states):
    monkeypatch.setattr(search_mod, "get_input", lambda _type, _prompt: "CA")
    assert search_mod.search_by_abbrev(dummy_states)["state"] == "California"


def test_search_by_abbrev_invalid_returns_none(monkeypatch, dummy_states, capsys):
    monkeypatch.setattr(search_mod, "get_input", lambda _type, _prompt: "ZZ")
    assert search_mod.search_by_abbrev(dummy_states) is None
    assert "Invalid state abbreviation" in capsys.readouterr().out


def test_search_by_name_returns_state(monkeypatch, dummy_states):
    monkeypatch.setattr(search_mod, "get_input", lambda _type, _prompt: "Texas")
    assert search_mod.search_by_name(dummy_states)["abbreviation"] == "TX"


def test_choose_from_list_uses_prompt(monkeypatch, dummy_states):
    monkeypatch.setattr(
        search_mod.Prompt, "menu", staticmethod(lambda options: "Florida")
    )
    assert search_mod.choose_from_list(dummy_states)["abbreviation"] == "FL"


def test_display_state_invalid_abbrev(dummy_states, capsys):
    search_mod.display_state("ZZ", dummy_states)
    assert "Invalid state abbreviation" in capsys.readouterr().out


def test_display_state_no_image(monkeypatch, dummy_states, capsys):
    monkeypatch.setattr(search_mod.os.path, "exists", lambda path: False)
    search_mod.display_state("CA", dummy_states)
    assert "No image found" in capsys.readouterr().out


def test_display_state_prints_info(monkeypatch, dummy_states, capsys):
    monkeypatch.setattr(search_mod.os.path, "exists", lambda path: True)

    class FakeImage:
        def draw(self):
            return None

    monkeypatch.setattr(search_mod, "from_file", lambda path: FakeImage())
    search_mod.display_state("CA", dummy_states)
    out = capsys.readouterr().out
    assert "State: California" in out
    assert "Population: 2,000" in out


def test_display_by_abbrev_calls_display_state(monkeypatch, dummy_states):
    called = []
    monkeypatch.setattr(
        search_mod,
        "search_by_abbrev",
        lambda states: dummy_states.get_state_by_abbreviation("CA"),
    )
    monkeypatch.setattr(
        search_mod, "display_state", lambda abbrev, states: called.append(abbrev)
    )
    search_mod.display_by_abbrev(dummy_states)
    assert called == ["CA"]
