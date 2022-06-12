import asyncio

import pytest
from flask_migrate import upgrade as flask_migrate_upgrade

from app import create_app, db
from tests.utils.structures import User
from tests.utils.testdata import Testdata

# @pytest.fixture(scope="session")
# def event_loop():
#     return asyncio.get_event_loop()


@pytest.fixture(scope="session")
def app():
    app = create_app()
    app.config.update(
        {
            "TESTING": True,
            'DEBUG': True,
        }
    )
    yield app


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
    res = {}
    user = testdata.create_user()
    response = client.post(
        "api/v1/auth/registration",
        json=user.dict(exclude={"id"}),
        headers={"content-type": "application/json"},
    )
    res['user'] = user
    res['access_token'] = response.json['access_token']
    res['refresh_token'] = response.json['refresh_token']
    return res
