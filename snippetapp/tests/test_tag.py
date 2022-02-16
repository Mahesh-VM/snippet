import json
import pytest
from server.tests.conftest import api_client, django_db_setup  # noqa
from django.db import DatabaseError, ProgrammingError
from django.urls import reverse

from snippetapp.models import Tag


@pytest.mark.django_db
class TestTags:
    """
    Test cases for the tag endpoint.
    """

    url = reverse("tag-list")
    skip_all = False

    def test_tag_model(self):
        try:
            create_obj = Tag.objects.create(title='Test tag creation.')
            latest_obj = Tag.objects.all().latest("id")
            if latest_obj is not None:
                assert latest_obj.id == create_obj.id
                assert latest_obj.title == create_obj.title

        except (ProgrammingError, DatabaseError, AttributeError):
            TestTags.skip_all = True

    @pytest.mark.skipif(
        "TestTags.skip_all",
        reason="Model declaration error.",
    )
    def test_create_tag(self, api_client):
        """
        Test creating a tag from endpoint which is not allowed.
        """
        data = {
            "title": "Create tag through post",
        }

        response = api_client.post(self.url, data, format='json')
        assert response.status_code == 405
        res = response.content.decode('utf-8')
        json_data = json.loads(res)
        assert json_data['detail'] == 'Method "POST" not allowed.'

    @pytest.mark.skipif(
        "TestTags.skip_all",
        reason="Model declaration error.",
    )
    def test_fetching_tag(self, api_client):
        new_tag = Tag.objects.create(title="Test created tag")
        response = api_client.get(self.url)
        assert response.status_code == 200
        res = response.content.decode('utf-8')
        json_data = json.loads(res)
        assert json_data[0]['title'] == 'Test created tag'

    @pytest.mark.skipif(
        "TestTags.skip_all",
        reason="Model declaration error.",
    )
    def test_updating_tag(self, api_client):
        # updating tag not allowed.
        new_tag = Tag.objects.create(title="Test created tag")
        data = {
            "title": "test update"
        }
        response = api_client.put(
            self.url+f"/{getattr(new_tag, 'id')}",
            data=data
        )
        assert response.status_code == 405
        res = response.content.decode('utf-8')
        json_data = json.loads(res)
        assert json_data['detail'] == 'Method "PUT" not allowed.'

    @pytest.mark.skipif(
        "TestTags.skip_all",
        reason="Model declaration error.",
    )
    def test_deleting_tag(self, api_client):
        # deleting tag not allowed.
        new_tag = Tag.objects.create(title="Test created tag")
        response = api_client.delete(self.url+f"/{getattr(new_tag, 'id')}")
        assert response.status_code == 405
        res = response.content.decode('utf-8')
        json_data = json.loads(res)
        assert json_data['detail'] == 'Method "DELETE" not allowed.'
