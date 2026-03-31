import pytest


@pytest.fixture
def sample_states():
    return [
        {
            "state": "California",
            "abbreviation": "CA",
            "capital": "Sacramento",
            "population": "39538223",
            "flower": "Golden Poppy",
        },
        {
            "state": "Texas",
            "abbreviation": "TX",
            "capital": "Austin",
            "population": "29145505",
            "flower": "Bluebonnet",
        },
        {
            "state": "Florida",
            "abbreviation": "FL",
            "capital": "Tallahassee",
            "population": "21538187",
            "flower": "Orange Blossom",
        },
    ]
