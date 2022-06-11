from http import HTTPStatus

from tests.utils.testdata import Testdata


def test_user_create(client, testdata: Testdata):
    user = testdata.create_user()
    response = client.post(
        "api/v1/auth/registration",
        json=user.dict(exclude={"id"}),
        headers={"content-type": "application/json"},
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json['status'] == True


def test_user_login(client, user_create):
    user = user_create["user"]
    response = client.post(
        "api/v1/auth/login",
        json=user.dict(include={"email", "password"}),
        headers={"content-type": "application/json"},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json['status'] == True


def test_refresh(client, user_create):
    user = user_create["user"]
    refresh_token = user_create["refresh_token"]
    response = client.post(
        "api/v1/auth/refresh",
        headers={
            "content-type": "application/json",
            "Authorization": "Bearer {}".format(refresh_token)
        }
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json['status'] == True


def test_refresh(client, user_create):
    access_token = user_create["access_token"]
    response = client.delete(
        "api/v1/auth/logout",
        headers={
            "content-type": "application/json",
            "Authorization": "Bearer {}".format(access_token)
        }
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json['status'] == True


def test_change(client, user_create, testdata):
    access_token = user_create["access_token"]
    new_user_data = testdata.create_user()
    response = client.post(
        "api/v1/auth/change",
        json=new_user_data.dict(exclude={"id"}),
        headers={
            "content-type": "application/json",
            "Authorization": "Bearer {}".format(access_token)
        }
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json['status'] == True


def test_history(client, user_create):
    access_token = user_create["access_token"]
    response = client.get(
        "api/v1/auth/history",
        headers={
            "content-type": "application/json",
            "Authorization": "Bearer {}".format(access_token)
        }
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json['status'] == True
