import pytest
from app import create_app
from app.models.user import User

@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    yield app

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

@pytest.fixture()
def user():
    return User("John", "Smith", "john@smith.com", "abcd1234!")
