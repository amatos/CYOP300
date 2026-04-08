import builtins

from lab4 import main as app


def test_main_calls_play_matrix_game_then_exits(monkeypatch, capsys):
    calls = {"played": 0}

    monkeypatch.setattr(
        app,
        "play_matrix_game",
        lambda: calls.__setitem__("played", calls["played"] + 1),
    )

    inputs = iter(["y", "n"])
    monkeypatch.setattr(builtins, "input", lambda prompt="": next(inputs))

    app.main()

    captured = capsys.readouterr()
    assert calls["played"] == 1
    assert "Welcome to the Python Matrix Application" in captured.out
    assert "Thanks for playing Python NumPy" in captured.out


def test_main_exits_immediately_on_n(monkeypatch, capsys):
    monkeypatch.setattr(builtins, "input", lambda prompt="": "n")

    app.main()

    captured = capsys.readouterr()
    assert "Thanks for playing Python NumPy" in captured.out


def test_main_reprompts_on_invalid_input(monkeypatch, capsys):
    inputs = iter(["invalid", "n"])
    monkeypatch.setattr(builtins, "input", lambda prompt="": next(inputs))

    app.main()

    captured = capsys.readouterr()
    assert "Invalid input. Please enter Y or N." in captured.out
