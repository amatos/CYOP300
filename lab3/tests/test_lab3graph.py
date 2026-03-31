import lab3.lab3graph


def test_plot_top_5_state_populations_sorts_and_plots(monkeypatch):
    sample_data = [
        {
            "state": "Texas",
            "abbreviation": "TX",
            "capital": "Austin",
            "population": "29145505",
            "flower": "Bluebonnet",
        },
        {
            "state": "California",
            "abbreviation": "CA",
            "capital": "Sacramento",
            "population": "39538223",
            "flower": "Golden Poppy",
        },
        {
            "state": "Florida",
            "abbreviation": "FL",
            "capital": "Tallahassee",
            "population": "21538187",
            "flower": "Orange Blossom",
        },
        {
            "state": "New York",
            "abbreviation": "NY",
            "capital": "Albany",
            "population": "20201249",
            "flower": "Rose",
        },
        {
            "state": "Pennsylvania",
            "abbreviation": "PA",
            "capital": "Harrisburg",
            "population": "13002700",
            "flower": "Mountain Laurel",
        },
        {
            "state": "Illinois",
            "abbreviation": "IL",
            "capital": "Springfield",
            "population": "12812508",
            "flower": "Violet",
        },
    ]

    class FakeStates:
        def __init__(self):
            self.state_data = sample_data

    monkeypatch.setattr(lab3.lab3graph.lab3states, "States", FakeStates)

    calls = {
        "subplots": False,
        "tight_layout": False,
        "show": False,
        "bar_args": None,
        "text_calls": [],
    }

    class FakeYAxis:
        def set_major_formatter(self, formatter):
            calls["formatter"] = formatter

    class FakeBar:
        def __init__(self, x, width, height):
            self._x = x
            self._width = width
            self._height = height

        def get_x(self):
            return self._x

        def get_width(self):
            return self._width

        def get_height(self):
            return self._height

    class FakeAxis:
        def bar(self, states, populations, color=None):
            calls["bar_args"] = (states, populations, color)
            return [
                FakeBar(0, 1, populations[0]),
                FakeBar(1, 1, populations[1]),
                FakeBar(2, 1, populations[2]),
                FakeBar(3, 1, populations[3]),
                FakeBar(4, 1, populations[4]),
            ]

        def set_title(self, title):
            calls["title"] = title

        def set_xlabel(self, label):
            calls["xlabel"] = label

        def set_ylabel(self, label):
            calls["ylabel"] = label

        @property
        def yaxis(self):
            return FakeYAxis()

        def tick_params(self, axis, rotation):
            calls["tick_params"] = (axis, rotation)

        def text(self, x, y, text, ha, va):
            calls["text_calls"].append((x, y, text, ha, va))

    class FakeFigure:
        pass

    def fake_subplots(figsize=None):
        calls["subplots"] = True
        calls["figsize"] = figsize
        return FakeFigure(), FakeAxis()

    monkeypatch.setattr(lab3.lab3graph.plt, "subplots", fake_subplots)
    monkeypatch.setattr(
        lab3.lab3graph.plt,
        "tight_layout",
        lambda: calls.__setitem__("tight_layout", True),
    )
    monkeypatch.setattr(
        lab3.lab3graph.plt, "show", lambda: calls.__setitem__("show", True)
    )

    lab3.lab3graph.plot_top_5_state_populations()

    assert calls["subplots"] is True
    assert calls["figsize"] == (10, 6)
    assert calls["bar_args"][0] == [
        "California",
        "Texas",
        "Florida",
        "New York",
        "Pennsylvania",
    ]
    assert calls["bar_args"][1] == [
        39538223,
        29145505,
        21538187,
        20201249,
        13002700,
    ]
    assert calls["bar_args"][2] == "green"
    assert calls["title"] == "Top 5 State Populations"
    assert calls["xlabel"] == "State"
    assert calls["ylabel"] == "Population"
    assert calls["tick_params"] == ("x", 45)
    assert calls["tight_layout"] is True
    assert calls["show"] is True
    assert len(calls["text_calls"]) == 5
