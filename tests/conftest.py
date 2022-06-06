import asyncio

import pytest
from utils.structures import User
from utils.testdata import Testdata

from app.app import create_app


@pytest.fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()


@pytest.fixture(scope="session")
def app():
    app = create_app()
    app.config.update(
        {
            "TESTING": True,
        }
    )

    # other setup can go here

    yield app

    # clean up / reset resources here


@pytest.fixture(scope="session")
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


@pytest.fixture(scope="session")
def testdata() -> Testdata:
    data = Testdata()
    return data


@pytest.fixture()
def user_create(client, testdata: Testdata) -> User:
    user = testdata.create_user()
    response = client.post(
        "api/v1/users/",
        json=user.dict(exclude={"id"}),
        headers={"content-type": "application/json"},
    )
    return User.parse_raw(response.json)
