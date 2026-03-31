import lab3.lab3search_states


def test_search_by_abbrev_found(monkeypatch, sample_states):
    monkeypatch.setattr(
        lab3.lab3search_states.lab3states, "States", lambda: FakeStates(sample_states)
    )
    monkeypatch.setattr(
        lab3.lab3search_states.lab3common, "get_input", lambda typ, prompt: "CA"
    )

    result = lab3.lab3search_states.search_by_abbrev()

    assert result["state"] == "California"


def test_search_by_abbrev_invalid(monkeypatch, sample_states, capsys):
    monkeypatch.setattr(
        lab3.lab3search_states.lab3states, "States", lambda: FakeStates(sample_states)
    )
    monkeypatch.setattr(
        lab3.lab3search_states.lab3common, "get_input", lambda typ, prompt: "ZZ"
    )

    result = lab3.lab3search_states.search_by_abbrev()

    assert result is None
    out = capsys.readouterr().out
    assert "Invalid state abbreviation" in out


def test_search_by_name_found(monkeypatch, sample_states):
    monkeypatch.setattr(
        lab3.lab3search_states.lab3states, "States", lambda: FakeStates(sample_states)
    )
    monkeypatch.setattr(
        lab3.lab3search_states.lab3common, "get_input", lambda typ, prompt: "Texas"
    )

    result = lab3.lab3search_states.search_by_name()

    assert result["abbreviation"] == "TX"


def test_choose_from_list(monkeypatch, sample_states):
    monkeypatch.setattr(
        lab3.lab3search_states.lab3states, "States", lambda: FakeStates(sample_states)
    )
    monkeypatch.setattr(
        lab3.lab3search_states.lab3prompt.Prompt,
        "menu",
        staticmethod(lambda options: "Florida"),
    )

    result = lab3.lab3search_states.choose_from_list()

    assert result["state"] == "Florida"


class FakeStates:
    def __init__(self, data):
        self.state_data = data

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
