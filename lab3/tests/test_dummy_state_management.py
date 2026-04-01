import pytest


@pytest.fixture
def dummy_states_data():
    return [
        {
            "state": "Alabama",
            "abbreviation": "AL",
            "capital": "Montgomery",
            "population": "1000",
            "flower": "Camellia",
        },
        {
            "state": "California",
            "abbreviation": "CA",
            "capital": "Sacramento",
            "population": "2000",
            "flower": "Poppy",
        },
        {
            "state": "Texas",
            "abbreviation": "TX",
            "capital": "Austin",
            "population": "3000",
            "flower": "Bluebonnet",
        },
        {
            "state": "Florida",
            "abbreviation": "FL",
            "capital": "Tallahassee",
            "population": "4000",
            "flower": "Orange Blossom",
        },
        {
            "state": "New York",
            "abbreviation": "NY",
            "capital": "Albany",
            "population": "5000",
            "flower": "Rose",
        },
        {
            "state": "Illinois",
            "abbreviation": "IL",
            "capital": "Springfield",
            "population": "6000",
            "flower": "Violet",
        },
    ]


@pytest.fixture
def dummy_state(dummy_states_data):
    return {
        "state": "Texas",
        "abbreviation": "TX",
        "capital": "Austin",
        "population": "3000",
        "flower": "Bluebonnet",
    }


class DummyStates:
    def __init__(self, state_data=None):
        self.state_data = state_data or []
        self.write_calls = []

    def __iter__(self):
        return iter(self.state_data)

    def get_state_by_abbreviation(self, abbrev):
        for state in self.state_data:
            if state["abbreviation"].lower() == abbrev.lower():
                return state
        return None

    def get_state_by_name(self, name):
        for state in self.state_data:
            if state["state"].lower() == name.lower():
                return state
        return None

    def write_state_data(self, data):
        self.write_calls.append(data)


@pytest.fixture
def dummy_states(dummy_states_data):
    return DummyStates(dummy_states_data)
