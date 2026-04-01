import lab3.lab3graph as graph


def test_plot_top_5_state_populations(monkeypatch, dummy_states):
    calls = {"show": 0, "tight": 0}

    class FakeText:
        def get_x(self):
            return 0

        def get_width(self):
            return 1

        def get_height(self):
            return 10

    class FakeAxis:
        def bar(self, labels, values, color=None):
            self.labels = labels
            self.values = values
            return [FakeText() for _ in values]

        def set_title(self, title):
            self.title = title

        def set_xlabel(self, label):
            self.xlabel = label

        def set_ylabel(self, label):
            self.ylabel = label

        @property
        def yaxis(self):
            class Y:
                def set_major_formatter(self, formatter):
                    self.formatter = formatter

            return Y()

        def tick_params(self, **kwargs):
            self.kwargs = kwargs

        def text(self, *args, **kwargs):
            return None

    class FakeFigure:
        pass

    fake_axis = FakeAxis()

    monkeypatch.setattr(
        graph.plt, "subplots", lambda figsize=None: (FakeFigure(), fake_axis)
    )
    monkeypatch.setattr(
        graph.plt, "tight_layout", lambda: calls.__setitem__("tight", 1)
    )
    monkeypatch.setattr(graph.plt, "show", lambda: calls.__setitem__("show", 1))

    graph.plot_top_5_state_populations(dummy_states)

    assert fake_axis.labels == [
        "Illinois",
        "New York",
        "Florida",
        "Texas",
        "California",
    ]
    assert calls["tight"] == 1
    assert calls["show"] == 1
