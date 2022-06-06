
from utils.testdata import Testdata


def test_user_create(client, testdata: Testdata):
    user = testdata.create_user()
    response = client.post(
        "api/v1/users/",
        json=user.dict(exclude={"id"}),
        headers={"content-type": "application/json"},
    )
    user.id = response.json["id"]
    assert response.status_code == 200
    return user


def test_user_delete(client, testdata: Testdata):
    user = testdata.create_user()
    response = client.delete("api/v1/users/{0}".format(user.id))
    assert response.status_code == 204


def test_user_update(client, testdata: Testdata):
    user = testdata.create_user()
    user_updated = testdata.create_user() 
    response = client.put(
        "api/v1/users/{0}".format(user.id),
        json=user.dict(exclude={"id"}),
        headers={"content-type": "application/json"},
    )
    assert response.status_code == 204


def test_user_get(client, user_create):
    response = client.get("api/v1/users/13")
    print(response.data)
    assert response.status_code == 200


b'{\n    "errors": {\n        "": "\'{\\"first_name\\": \\"\\\\\\\\u041c\\\\\\\\u043e\\\\\\\\u043a\\\\\\\\u0435\\\\\\\\u0439\\", \\"last_name\\": \\"\\\\\\\\u042f\\\\\\\\u043a\\\\\\\\u043e\\\\\\\\u0432\\\\\\\\u043b\\\\\\\\u0435\\\\\\\\u0432\\\\\\\\u0430\\", \\"password\\": \\"@T6YM4OsOw\\", \\"email\\": \\"jakovlevvladilen@rambler.ru\\"}\' is not of type \'object\'"\n    },\n    "message": "Input payload validation failed"\n}\n'
