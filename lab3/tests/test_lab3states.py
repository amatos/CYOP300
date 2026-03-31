import io
from unittest.mock import mock_open

import pytest

import lab3.lab3states


@pytest.fixture
def sample_states():
    return [
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
    ]


def test_load_state_data_uses_us_states_csv_when_no_modified_file(monkeypatch):
    csv_text = (
        "state,abbreviation,capital,population,flower\n"
        "Texas,TX,Austin,29145505,Bluebonnet\n"
        "California,CA,Sacramento,39538223,Golden Poppy\n"
        "Florida,FL,Tallahassee,21538187,Orange Blossom\n"
    )

    monkeypatch.setattr(lab3.lab3states.os.path, "exists", lambda path: False)
    monkeypatch.setattr("builtins.open", mock_open(read_data=csv_text))

    result = lab3.lab3states.States.load_state_data()

    assert [row["state"] for row in result] == ["California", "Florida", "Texas"]


def test_load_state_data_uses_modified_file_if_present(monkeypatch):
    csv_text = (
        "state,abbreviation,capital,population,flower\n"
        "Nevada,NV,Carson City,3104614,Sagebrush\n"
        "Alaska,AK,Juneau,733391,Forget-Me-Not\n"
    )

    def fake_exists(path):
        return path.endswith("us_states_modified.csv")

    monkeypatch.setattr(lab3.lab3states.os.path, "exists", fake_exists)
    monkeypatch.setattr("builtins.open", mock_open(read_data=csv_text))

    result = lab3.lab3states.States.load_state_data()

    assert [row["state"] for row in result] == ["Alaska", "Nevada"]


def test_get_state_by_abbreviation_is_case_insensitive(monkeypatch, sample_states):
    monkeypatch.setattr(
        lab3.lab3states.States, "load_state_data", staticmethod(lambda: sample_states)
    )

    states = lab3.lab3states.States()
    result = states.get_state_by_abbreviation("ca")

    assert result is not None
    assert result["state"] == "California"


def test_get_state_by_abbreviation_returns_none_when_missing(
    monkeypatch, sample_states
):
    monkeypatch.setattr(
        lab3.lab3states.States, "load_state_data", staticmethod(lambda: sample_states)
    )

    states = lab3.lab3states.States()
    result = states.get_state_by_abbreviation("ZZ")

    assert result is None


def test_get_state_by_name_is_case_insensitive(monkeypatch, sample_states):
    monkeypatch.setattr(
        lab3.lab3states.States, "load_state_data", staticmethod(lambda: sample_states)
    )

    states = lab3.lab3states.States()
    result = states.get_state_by_name("texas")

    assert result is not None
    assert result["abbreviation"] == "TX"


def test_get_state_by_name_returns_none_when_missing(monkeypatch, sample_states):
    monkeypatch.setattr(
        lab3.lab3states.States, "load_state_data", staticmethod(lambda: sample_states)
    )

    states = lab3.lab3states.States()
    result = states.get_state_by_name("NotAState")

    assert result is None


def test_update_state_population_updates_state_and_writes(monkeypatch, sample_states):
    monkeypatch.setattr(
        lab3.lab3states.States, "load_state_data", staticmethod(lambda: sample_states)
    )

    write_calls = {"called": False, "data": None}

    def fake_write_state_data(data):
        write_calls["called"] = True
        write_calls["data"] = data

    monkeypatch.setattr(
        lab3.lab3states.States, "write_state_data", staticmethod(fake_write_state_data)
    )

    states = lab3.lab3states.States()
    result = states.update_state_population("Texas", 99999999)

    assert result is True
    assert states.get_state_by_name("Texas")["population"] == "99999999"
    assert write_calls["called"] is True
    assert write_calls["data"] == states.state_data


def test_update_state_population_returns_false_for_missing_state(
    monkeypatch, sample_states
):
    monkeypatch.setattr(
        lab3.lab3states.States, "load_state_data", staticmethod(lambda: sample_states)
    )

    states = lab3.lab3states.States()
    result = states.update_state_population("Maine", 12345)

    assert result is False
