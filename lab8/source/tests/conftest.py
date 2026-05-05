import app
import pytest


@pytest.fixture
def client():
    app.app.config["TESTING"] = True
    app.app.config["WTF_CSRF_ENABLED"] = False

    with app.app.test_client() as client:
        yield client


@pytest.fixture
def logged_in_client(client):
    with client.session_transaction() as session:
        session["username"] = "user@example.com"
        session["is_admin"] = False
    return client


@pytest.fixture
def admin_client(client):
    with client.session_transaction() as session:
        session["username"] = "admin"
        session["is_admin"] = True
    return client
