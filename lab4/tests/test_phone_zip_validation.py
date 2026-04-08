import builtins

from lab4 import phone_and_zip as paz


def test_validate_value_accepts_matching_pattern():
    assert paz.validate_value("123-456-7890", r"^\d{3}-\d{3}-\d{4}$") is True


def test_validate_value_rejects_non_matching_pattern():
    assert paz.validate_value("1234567890", r"^\d{3}-\d{3}-\d{4}$") is False


def test_get_phone_accepts_valid_input(monkeypatch):
    monkeypatch.setattr(builtins, "input", lambda prompt="": "123-456-7890")
    assert paz.get_phone() == "123-456-7890"


def test_get_phone_reprompts_until_valid(monkeypatch, capsys):
    inputs = iter(["bad input", "123-456-7890"])
    monkeypatch.setattr(builtins, "input", lambda prompt="": next(inputs))

    result = paz.get_phone()

    captured = capsys.readouterr()
    assert result == "123-456-7890"
    assert "Your phone number is not in correct format" in captured.out


def test_get_zipcode_accepts_valid_input(monkeypatch):
    monkeypatch.setattr(builtins, "input", lambda prompt="": "12345-6789")
    assert paz.get_zipcode() == "12345-6789"


def test_get_zipcode_reprompts_until_valid(monkeypatch, capsys):
    inputs = iter(["1234-5678", "12345-6789"])
    monkeypatch.setattr(builtins, "input", lambda prompt="": next(inputs))

    result = paz.get_zipcode()

    captured = capsys.readouterr()
    assert result == "12345-6789"
    assert "Your zip code is not in correct format" in captured.out
