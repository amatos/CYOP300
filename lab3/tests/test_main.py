import lab3.main


def test_display_states(monkeypatch, capsys, sample_states):
    monkeypatch.setattr(
        lab3.main.lab3states, "States", lambda: FakeStates(sample_states)
    )
    monkeypatch.setattr(lab3.main.lab3prompt, "reprompt_menu", lambda func: None)

    lab3.main.display_states()

    out = capsys.readouterr().out
    assert "Displaying all U.S. States" in out
    assert "California" in out


def test_graph_bar_calls_graph(monkeypatch):
    called = {"plot": False}

    monkeypatch.setattr(
        lab3.main.lab3graph,
        "plot_top_5_state_populations",
        lambda: called.__setitem__("plot", True),
    )
    monkeypatch.setattr(lab3.main.lab3prompt, "reprompt_menu", lambda func: None)

    lab3.main.graph_bar()

    assert called["plot"] is True


def test_update_state_population(monkeypatch, capsys):
    monkeypatch.setattr(
        lab3.main.lab3prompt.Prompt, "dict_menu", staticmethod(lambda options: None)
    )
    monkeypatch.setattr(lab3.main.lab3prompt, "reprompt_menu", lambda func: None)

    lab3.main.update_state_population()

    out = capsys.readouterr().out
    assert "Updating the overall state population" in out


class FakeStates:
    def __init__(self, data):
        self.state_data = data
