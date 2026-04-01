import lab3.lab3modify_pop as modify_pop


def test_modify_state_population_updates_and_saves(monkeypatch, dummy_states, capsys):
    state = dummy_states.get_state_by_name("Texas")

    monkeypatch.setattr(modify_pop, "States", lambda: dummy_states)
    monkeypatch.setattr(modify_pop, "get_input", lambda _type, _prompt: 12345)
    monkeypatch.setattr(modify_pop, "get_yes_no_input", lambda prompt="": "y")

    modify_pop.modify_state_population(state)

    out = capsys.readouterr().out
    assert "Current population of Texas: 3,000" in out
    assert "New population of Texas: 12,345" in out
    assert dummy_states.get_state_by_name("Texas")["population"] == 12345
    assert dummy_states.write_calls


def test_modify_state_population_none(capsys, monkeypatch, dummy_states):
    monkeypatch.setattr(modify_pop, "States", lambda: dummy_states)
    modify_pop.modify_state_population(None)
    assert "State not found" in capsys.readouterr().out
