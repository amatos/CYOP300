import lab3.lab3states as states_mod


def test_states_getters_and_update(monkeypatch):
    dummy = states_mod.States.__new__(states_mod.States)
    dummy.state_data = [
        {"state": "Texas", "abbreviation": "TX", "population": "3000"},
        {"state": "California", "abbreviation": "CA", "population": "2000"},
    ]
    monkeypatch.setattr(states_mod.States, "write_state_data", lambda self, data: None)

    assert states_mod.States.get_state_by_abbreviation(dummy, "tx")["state"] == "Texas"
    assert states_mod.States.get_state_by_name(dummy, "california")["abbreviation"] == "CA"
    assert states_mod.States.update_state_population(dummy, "Texas", 9999) is True
    assert dummy.state_data[0]["population"] == "9999"
    assert states_mod.States.update_state_population(dummy, "Nevada", 1) is False
