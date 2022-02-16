import json
import pytest
from server.tests.conftest import api_client, django_db_setup  # noqa
from django.urls import reverse


@pytest.mark.django_db
class TestTags:
    """
    Test cases for the tag endpoint.
    """

    url = reverse("register")

    def test_register_user(self, api_client):
        data = {
            "email": "test@gmail.com",
            "password": "test1223",
            "confirm_password": "test1223",
            "roles": "user",
            "first_name": "Test",
            "last_name": "user one",
            "username": "user_one"
        }

        response = api_client.post(self.url, data)
        assert response.status_code == 201
        res = response.content.decode('utf-8')
        json_data = json.loads(res)
        print("json", json_data)
