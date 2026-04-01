import lab3.lab3search_states as search_mod


class DummyStates:
    def __init__(self, state_data=None):
        self.state_data = state_data or [
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
        ]

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


def test_search_by_abbrev_returns_state(monkeypatch):
    dummy = DummyStates()
    monkeypatch.setattr(search_mod, "get_input", lambda _type, _prompt: "CA")
    assert search_mod.search_by_abbrev(dummy)["state"] == "California"


def test_search_by_abbrev_invalid_returns_none(monkeypatch, capsys):
    dummy = DummyStates()
    monkeypatch.setattr(search_mod, "get_input", lambda _type, _prompt: "ZZ")
    assert search_mod.search_by_abbrev(dummy) is None
    assert "Invalid state abbreviation" in capsys.readouterr().out


def test_search_by_name_returns_state(monkeypatch):
    dummy = DummyStates()
    monkeypatch.setattr(search_mod, "get_input", lambda _type, _prompt: "Texas")
    assert search_mod.search_by_name(dummy)["abbreviation"] == "TX"


def test_choose_from_list_uses_prompt(monkeypatch):
    dummy = DummyStates()
    monkeypatch.setattr(search_mod.Prompt, "menu", staticmethod(lambda options: "Florida"))
    assert search_mod.choose_from_list(dummy)["abbreviation"] == "FL"


def test_display_state_invalid_abbrev(monkeypatch, capsys):
    dummy = DummyStates()
    search_mod.display_state("ZZ", dummy)
    assert "Invalid state abbreviation" in capsys.readouterr().out


def test_display_state_no_image(monkeypatch, capsys):
    dummy = DummyStates()
    monkeypatch.setattr(search_mod.os.path, "exists", lambda path: False)
    search_mod.display_state("CA", dummy)
    assert "No image found" in capsys.readouterr().out


def test_display_state_prints_info(monkeypatch, capsys):
    dummy = DummyStates()
    monkeypatch.setattr(search_mod.os.path, "exists", lambda path: True)

    class FakeImage:
        def draw(self):
            return None

    monkeypatch.setattr(search_mod, "from_file", lambda path: FakeImage())
    search_mod.display_state("CA", dummy)
    out = capsys.readouterr().out
    assert "State: California" in out
    assert "Population: 2,000" in out


def test_display_by_abbrev_calls_display_state(monkeypatch):
    dummy = DummyStates()
    called = []
    monkeypatch.setattr(search_mod, "search_by_abbrev", lambda states: dummy.get_state_by_abbreviation("CA"))
    monkeypatch.setattr(search_mod, "display_state", lambda abbrev, states: called.append(abbrev))
    search_mod.display_by_abbrev(dummy)
    assert called == ["CA"]
