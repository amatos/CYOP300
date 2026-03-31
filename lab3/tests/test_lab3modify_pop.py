import lab3.lab3modify_pop


def test_modify_state_population_updates_and_saves(monkeypatch, sample_states, capsys):
    monkeypatch.setattr(
        lab3.lab3modify_pop.lab3states, "States", lambda: FakeStates(sample_states)
    )
    monkeypatch.setattr(
        lab3.lab3modify_pop.lab3common, "get_input", lambda typ, prompt: 999
    )
    monkeypatch.setattr(
        lab3.lab3modify_pop.lab3common, "get_yes_no_input", lambda prompt: "y"
    )

    lab3.lab3modify_pop.modify_state_population(
        {"state": "Texas", "population": "29145505"}
    )

    out = capsys.readouterr().out
    assert "Current population of Texas" in out
    assert "New population of Texas" in out


def test_modify_state_population_none(monkeypatch, capsys):
    monkeypatch.setattr(
        lab3.lab3modify_pop.lab3states, "States", lambda: FakeStates([])
    )

    lab3.lab3modify_pop.modify_state_population(None)

    out = capsys.readouterr().out
    assert "State not found" in out


class FakeStates:
    def __init__(self, data):
        self.state_data = data
        self.saved = False

    def __iter__(self):
        return iter(self.state_data)

    def write_state_data(self, data):
        self.saved = True
