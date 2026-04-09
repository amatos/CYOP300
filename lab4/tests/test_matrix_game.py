import builtins

import numpy as np

from lab4 import matrix_game as mg


def test_parse_matrix_row_accepts_valid_integer_row():
    assert mg.parse_matrix_row("1 2 3") == [1.0, 2.0, 3.0]


def test_parse_matrix_row_accepts_valid_float_row():
    assert mg.parse_matrix_row("1.5 2 3.25") == [1.5, 2.0, 3.25]


def test_parse_matrix_row_rejects_wrong_number_of_values():
    assert mg.parse_matrix_row("1 2") is None
    assert mg.parse_matrix_row("1 2 3 4") is None


def test_parse_matrix_row_rejects_non_numeric_values():
    assert mg.parse_matrix_row("1 x 3") is None


def test_matrix_add_returns_elementwise_sum():
    a = np.array([[1, 2], [3, 4]])
    b = np.array([[5, 6], [7, 8]])

    result = mg.matrix_add(a, b)

    assert np.array_equal(result, np.array([[6, 8], [10, 12]]))


def test_matrix_subtract_returns_elementwise_difference():
    a = np.array([[5, 6], [7, 8]])
    b = np.array([[1, 2], [3, 4]])

    result = mg.matrix_subtract(a, b)

    assert np.array_equal(result, np.array([[4, 4], [4, 4]]))


def test_matrix_multiply_returns_matrix_product():
    a = np.array([[1, 2], [3, 4]])
    b = np.array([[5, 6], [7, 8]])

    result = mg.matrix_multiply(a, b)

    assert np.array_equal(result, np.array([[19, 22], [43, 50]]))


def test_matrix_element_multiply_returns_elementwise_product():
    a = np.array([[1, 2], [3, 4]])
    b = np.array([[5, 6], [7, 8]])

    result = mg.matrix_element_multiply(a, b)

    assert np.array_equal(result, np.array([[5, 12], [21, 32]]))


def test_get_operation_choice_reprompts_until_valid(monkeypatch, capsys):
    inputs = iter(["x", "d"])
    monkeypatch.setattr(builtins, "input", lambda prompt="": next(inputs))

    result = mg.get_operation_choice()

    captured = capsys.readouterr()
    assert result == "d"
    assert "Invalid choice. Please enter a, b, c, or d." in captured.out


def test_get_matrix_reprompts_for_invalid_rows(monkeypatch, capsys):
    inputs = iter(
        [
            "1 2",  # invalid
            "1 2 3",  # valid row 1
            "a b c",  # invalid
            "4 5 6",  # valid row 2
            "7 8 9",  # valid row 3
        ]
    )
    monkeypatch.setattr(builtins, "input", lambda prompt="": next(inputs))

    result = mg.get_matrix("first")

    captured = capsys.readouterr()
    assert np.array_equal(
        result, np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]])
    )
    assert (
        captured.out.count(
            "Invalid input. Please enter 3 numeric values separated by spaces."
        )
        == 2
    )


def test_display_matrix_shows_integers_without_decimals(capsys):
    matrix = np.array([[1, 2], [3, 4]])

    mg.display_matrix(matrix, label="My Matrix")

    captured = capsys.readouterr()
    assert "My Matrix" in captured.out
    assert "1 2" in captured.out
    assert "3 4" in captured.out


def test_display_results_prints_summary(monkeypatch, capsys):
    monkeypatch.setattr(
        mg, "display_matrix", lambda matrix, label="": print("DISPLAYED")
    )

    result = np.array([[1, 2], [3, 4]])
    mg.display_results(result, "Addition")

    captured = capsys.readouterr()
    assert "You selected Addition. The results are:" in captured.out
    assert captured.out.count("DISPLAYED") == 2
    assert "The Transpose is:" in captured.out
    assert "  Row means    :" in captured.out
    assert "  Column means :" in captured.out


def test_play_matrix_game_runs_addition_flow(monkeypatch, capsys):
    monkeypatch.setattr(mg, "get_phone", lambda: "123-456-7890")
    monkeypatch.setattr(mg, "get_zipcode", lambda: "12345-6789")
    monkeypatch.setattr(
        mg, "get_matrix", lambda label: np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    )
    monkeypatch.setattr(mg, "get_operation_choice", lambda: "a")

    calls = {"display_results": 0, "result": None, "operation_name": None}

    def fake_display_results(result, operation_name):
        calls["display_results"] += 1
        calls["result"] = result
        calls["operation_name"] = operation_name

    monkeypatch.setattr(mg, "display_results", fake_display_results)

    mg.play_matrix_game()

    captured = capsys.readouterr()
    assert "Phone number accepted: 123-456-7890" in captured.out
    assert "Zip code accepted: 12345-6789" in captured.out
    assert calls["display_results"] == 1
    assert calls["operation_name"] == "Addition"
    assert np.array_equal(
        calls["result"], np.array([[2, 4, 6], [8, 10, 12], [14, 16, 18]])
    )
