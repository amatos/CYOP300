import datetime
import math
import sys

import pytest

from lab2 import main


def test_generate_secure_password_success(monkeypatch, capsys):
    monkeypatch.setattr(
        main.lab2passwd,
        "build_password_requirements",
        lambda: (8, {"upper": 1, "lower": 1, "digits": 1, "special": 1}, "abcd"),
    )
    monkeypatch.setattr(main.lab2passwd, "generate_password", lambda *args: "Ab3!")
    monkeypatch.setattr(
        main.lab2passwd,
        "count_character_types",
        lambda password: {"upper": 1, "lower": 1, "digits": 1, "special": 1},
    )
    monkeypatch.setattr(
        main.lab2prompt.Prompt, "dict_menu", staticmethod(lambda options: None)
    )

    main.generate_secure_password()

    out = capsys.readouterr().out
    assert "Your secure password is: Ab3!" in out
    assert "1 upper characters" in out
    assert "1 lower characters" in out
    assert "1 digits characters" in out
    assert "1 special characters" in out


def test_generate_secure_password_handles_value_error(monkeypatch, capsys):
    monkeypatch.setattr(
        main.lab2passwd,
        "build_password_requirements",
        lambda: (_ for _ in ()).throw(ValueError("too short")),
    )
    monkeypatch.setattr(
        main.lab2prompt.Prompt, "dict_menu", staticmethod(lambda options: None)
    )

    main.generate_secure_password()

    out = capsys.readouterr().out
    assert "Invalid input: too short" in out
    assert "Please try again." in out


def test_calculate_percentage(monkeypatch, capsys):
    values = iter([12.5, 50.0, 2])

    monkeypatch.setattr(
        main.lab2common, "get_input", lambda _type, prompt: next(values)
    )
    monkeypatch.setattr(
        main.lab2prompt.Prompt, "dict_menu", staticmethod(lambda options: None)
    )

    main.calculate_percentage()

    out = capsys.readouterr().out
    assert "Enter the numerator, denominator, and decimal places:" in out
    assert "12.5/50.0 = 25.00 %" in out


def test_calculate_days_until_july_4_past(monkeypatch, capsys):
    class FakeDate(datetime.date):
        @classmethod
        def today(cls):
            return cls(2025, 7, 5)

    monkeypatch.setattr(main.datetime, "date", FakeDate)
    monkeypatch.setattr(
        main.lab2prompt.Prompt, "dict_menu", staticmethod(lambda options: None)
    )

    main.calculate_days_until_july_4()

    out = capsys.readouterr().out
    assert "July 4, 2025 occurred 1 days ago." in out


def test_calculate_days_until_july_4_future(monkeypatch, capsys):
    class FakeDate(datetime.date):
        @classmethod
        def today(cls):
            return cls(2025, 7, 1)

    monkeypatch.setattr(main.datetime, "date", FakeDate)
    monkeypatch.setattr(
        main.lab2prompt.Prompt, "dict_menu", staticmethod(lambda options: None)
    )

    main.calculate_days_until_july_4()

    out = capsys.readouterr().out
    assert "There are 3 days until July 4, 2025." in out


def test_calculate_triangle_leg(monkeypatch, capsys):
    values = iter([3.0, 4.0, 90.0])

    monkeypatch.setattr(
        main.lab2common, "get_input", lambda _type, prompt: next(values)
    )
    monkeypatch.setattr(
        main.lab2prompt.Prompt, "dict_menu", staticmethod(lambda options: None)
    )

    main.calculate_triangle_leg()

    out = capsys.readouterr().out
    assert "Enter the lengths of the sides of the triangle:" in out
    assert "The length of the leg of the triangle is: 5.00" in out


def test_calculate_cylinder_volume(monkeypatch, capsys):
    monkeypatch.setattr(
        main.lab2common, "get_input_in_mm", lambda value_type, prompt: (5.0, "cm")
    )
    monkeypatch.setattr(
        main.lab2prompt.Prompt, "dict_menu", staticmethod(lambda options: None)
    )

    main.calculate_cylinder_volume()

    out = capsys.readouterr().out
    expected_volume = math.pi * 5.0**2 * 5.0
    assert "Enter the radius and height of the cylinder:" in out
    assert f"The volume of the cylinder is: {expected_volume:.2f} mm^3" in out


def test_exit_program_raises_system_exit(monkeypatch, capsys):
    with pytest.raises(SystemExit) as excinfo:
        main.exit_program()

    out = capsys.readouterr().out
    assert "Exiting program. Thank you for using me!" in out
    assert excinfo.value.code == 0


def test_main_dispatches_menu(monkeypatch):
    captured = {}

    def fake_dict_menu(options):
        captured["keys"] = list(options.keys())

    monkeypatch.setattr(
        main.lab2prompt.Prompt, "dict_menu", staticmethod(fake_dict_menu)
    )

    main.main()

    assert "a. Generate Secure Password" in captured["keys"]
    assert "f. Exit program" in captured["keys"]
