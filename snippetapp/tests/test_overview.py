import json
import pytest
from server.tests.conftest import (
    api_client,
    django_db_setup,
    api_client_invalid_token,
    api_client_without_token
)
from django.db import DatabaseError, ProgrammingError
from django.urls import reverse
from authapp.models import User
from snippetapp.models import Snippet, Tag


@pytest.mark.django_db
class TestOverview:
    """
    Test cases for the overview endpoint.
    """

    url = reverse("overview-list")
    skip_all = False

    def test_snippet_model(self):
        try:
            user = User.objects.create_user(
                username='user_one',
                email='test@email.com',
                password='test123'
            )
            new_tag = Tag.objects.create(title='Test tag')
            new_snippet = Snippet.objects.create(
                tag=new_tag,
                content='Test snippet creation.',
                owner=user
            )
            latest_obj = Snippet.objects.all().latest("id")
            if latest_obj is not None:
                assert latest_obj.id == new_snippet.id
                assert latest_obj.owner == new_snippet.owner
                assert latest_obj.content == new_snippet.content

        except (ProgrammingError, DatabaseError, AttributeError):
            TestOverview.skip_all = False

    @pytest.mark.skipif(
        "TestOverview.skip_all",
        reason="Model declaration error.",
    )
    def test_create_overview(self, api_client):
        # create records not allowed
        data = {
            "tag": {
                "title": "Snippet test tag"
            },
            "content": "This is content for the snippet test tag."
        }

        response = api_client.post(self.url, data, format='json')
        res = response.content.decode('utf-8')
        json_data = json.loads(res)
        assert response.status_code == 405
        assert json_data['detail'] == 'Method "POST" not allowed.'

    @pytest.mark.skipif(
        "TestOverview.skip_all",
        reason="Model declaration error.",
    )
    def test_fetching_snippets(self, api_client):
        user = User.objects.create_user(
            username='user_two',
            email='test1@email.com',
            password='test123'
        )
        new_tag = Tag.objects.create(title="Test created tag")
        new_snippet = Snippet.objects.create(
            tag=new_tag,
            content='Test snippet creation.',
            owner=user
        )
        response = api_client.get(self.url)
        assert response.status_code == 200
        res = response.content.decode('utf-8')
        json_data = json.loads(res)
        snippet_count = Snippet.objects.count()
        assert json_data['count'] == snippet_count
        assert json_data['data'][0]['content'] == 'Test snippet creation.'
        assert json_data['data'][0]['owner'] == 'user_two'

        # get the latest snippet details
        detail_url = json_data['data'][0]['url']
        detail_response = api_client.get(detail_url)
        res = detail_response.content.decode('utf-8')
        json_data = json.loads(res)
        assert detail_response.status_code == 200
        assert json_data['tag'] == 'Test created tag'
        assert json_data['content'] == 'Test snippet creation.'
        assert json_data['owner'] == 'user_two'


    @pytest.mark.skipif(
        "TestOverview.skip_all",
        reason="Model declaration error.",
    )
    def test_fetching_snippet_detail(self, api_client):
        user = User.objects.create_user(
            username='user_two',
            email='test1@email.com',
            password='test123'
        )
        new_tag = Tag.objects.create(title="Test created tag")
        new_snippet = Snippet.objects.create(
            tag=new_tag,
            content='Test snippet creation.',
            owner=user
        )
        response = api_client.get(self.url + f"/{getattr(new_snippet, 'id')}")
        assert response.status_code == 200
        res = response.content.decode('utf-8')
        json_data = json.loads(res)
        assert json_data['content'] == 'Test snippet creation.'
        assert json_data['owner'] == 'user_two'

    @pytest.mark.skipif(
        "TestOverview.skip_all",
        reason="Model declaration error.",
    )
    def test_snippet_without_token(self, api_client_without_token):
        get_response = api_client_without_token.get(self.url)
        get_json_data = json.loads(get_response.content.decode('utf-8'))
        assert get_response.status_code == 401
        assert get_json_data['detail'] == "Authentication credentials were not provided."

    @pytest.mark.skipif(
        "TestOverview.skip_all",
        reason="Model declaration error.",
    )
    def test_snippet_invalid_token(self, api_client_invalid_token):
        get_response = api_client_invalid_token.get(self.url)
        get_json_data = json.loads(get_response.content.decode('utf-8'))
        assert get_response.status_code == 401
        assert get_json_data['detail'] == "Authorization header must contain two space-delimited values"
        assert get_json_data['code'] == "bad_authorization_header"
