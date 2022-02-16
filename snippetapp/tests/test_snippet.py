import json
import pytest
from server.tests.conftest import (
    api_client,
    django_db_setup,
    api_client_without_token,
    api_client_invalid_token
)
from django.db import DatabaseError, ProgrammingError
from django.urls import reverse
from authapp.models import User
from snippetapp.models import Snippet, Tag
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.mark.django_db
class TestSnippets:
    """
    Test cases for the snippet endpoint.
    """

    url = reverse("snippet-list")
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
            TestSnippets.skip_all = False

    @pytest.mark.skipif(
        "TestSnippets.skip_all",
        reason="Model declaration error.",
    )
    def test_create_snippet(self, api_client):
        data = {
            "tag": {
                "title": "Snippet test tag"
            },
            "content": "This is content for the snippet test tag."
        }

        response = api_client.post(self.url, data, format='json')
        res = response.content.decode('utf-8')
        json_data = json.loads(res)
        assert response.status_code == 201
        assert json_data['tag'] == "Snippet test tag"
        assert json_data['content'] == "This is content for the snippet test tag."
        assert json_data['owner'] == "user_one"

    @pytest.mark.skipif(
        "TestSnippets.skip_all",
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
        assert json_data[0]['tag'] == 'Test created tag'
        assert json_data[0]['content'] == 'Test snippet creation.'
        assert json_data[0]['owner'] == 'user_two'


    @pytest.mark.skipif(
        "TestSnippets.skip_all",
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
        assert json_data['tag'] == 'Test created tag'
        assert json_data['content'] == 'Test snippet creation.'
        assert json_data['owner'] == 'user_two'


    @pytest.mark.skipif(
        "TestSnippets.skip_all",
        reason="Model declaration error.",
    )
    def test_updating_snippet(self, api_client):
        user = User.objects.create_user(
            username='user_two',
            email='test1@email.com',
            password='test123'
        )
        refresh = RefreshToken.for_user(user)
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
        assert json_data[0]['tag'] == 'Test created tag'
        assert json_data[0]['content'] == 'Test snippet creation.'
        assert json_data[0]['owner'] == 'user_two'
        data = {
            "tag": {
                "title": "Test updated tag"
            },
            "content": "Test snippet updation."
        }
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        put_response = api_client.put(
            self.url + f"/{getattr(new_snippet, 'id')}",
            data=data,
            format='json'
        )
        res = put_response.content.decode('utf-8')
        json_data = json.loads(res)
        assert put_response.status_code == 200
        assert json_data['tag'] == 'Test updated tag'
        assert json_data['content'] == 'Test snippet updation.'
        assert json_data['owner'] == 'user_two'

    @pytest.mark.skipif(
        "TestSnippets.skip_all",
        reason="Model declaration error.",
    )
    def test_updating_snippet_with_incomplete_parameters(self, api_client):
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
        assert json_data[0]['tag'] == 'Test created tag'
        assert json_data[0]['content'] == 'Test snippet creation.'
        assert json_data[0]['owner'] == 'user_two'
        data = {
            "content": "Test snippet updation."
        }
        put_response = api_client.put(
            self.url + f"/{getattr(new_snippet, 'id')}",
            data=data,
            format='json'
        )
        res = put_response.content.decode('utf-8')
        json_data = json.loads(res)
        assert put_response.status_code == 400
        assert json_data['tag'] == ['This field is required.']

    @pytest.mark.skipif(
        "TestSnippets.skip_all",
        reason="Model declaration error.",
    )
    def test_updating_snippet_with_another_user(self, api_client):
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
        assert json_data[0]['tag'] == 'Test created tag'
        assert json_data[0]['content'] == 'Test snippet creation.'
        assert json_data[0]['owner'] == 'user_two'
        data = {
            "tag": {
                "title": "Test updated tag"
            },
            "content": "Test snippet updation."
        }
        put_response = api_client.put(
            self.url + f"/{getattr(new_snippet, 'id')}",
            data=data,
            format='json'
        )
        res = put_response.content.decode('utf-8')
        json_data = json.loads(res)
        assert put_response.status_code == 200
        assert json_data['tag'] == 'Test updated tag'
        assert json_data['content'] == 'Test snippet updation.'
        assert json_data['owner'] == 'user_one'

    @pytest.mark.skipif(
        "TestSnippets.skip_all",
        reason="Model declaration error.",
    )
    def test_patching_snippet(self, api_client):
        user = User.objects.create_user(
            username='user_three',
            email='test3@email.com',
            password='test123'
        )
        refresh = RefreshToken.for_user(user)
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
        assert json_data[0]['tag'] == 'Test created tag'
        assert json_data[0]['content'] == 'Test snippet creation.'
        assert json_data[0]['owner'] == 'user_three'

        data = {
            "content": "Test snippet patching."
        }
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        patch_response = api_client.patch(
            self.url + f"/{getattr(new_snippet, 'id')}",
            data=data,
            format='json'
        )
        details = patch_response.content.decode('utf-8')
        json_data = json.loads(details)
        assert patch_response.status_code == 200
        assert json_data['tag'] == 'Test created tag'
        assert json_data['content'] == 'Test snippet patching.'
        assert json_data['owner'] == 'user_three'

    @pytest.mark.skipif(
        "TestSnippets.skip_all",
        reason="Model declaration error.",
    )
    def test_patching_snippet_with_another_user(self, api_client):
        user = User.objects.create_user(
            username='user_three',
            email='test3@email.com',
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
        assert json_data[0]['tag'] == 'Test created tag'
        assert json_data[0]['content'] == 'Test snippet creation.'
        assert json_data[0]['owner'] == 'user_three'

        data = {
            "content": "Test snippet patching."
        }
        patch_response = api_client.patch(
            self.url + f"/{getattr(new_snippet, 'id')}",
            data=data,
            format='json'
        )
        detail = patch_response.content.decode('utf-8')
        json_data = json.loads(detail)
        assert patch_response.status_code == 200
        assert json_data['tag'] == 'Test created tag'
        assert json_data['content'] == 'Test snippet patching.'
        assert json_data['owner'] == 'user_one'


    @pytest.mark.skipif(
        "TestSnippets.skip_all",
        reason="Model declaration error.",
    )
    def test_deleting_snippet(self, api_client):
        user = User.objects.create_user(
            username='user_three',
            email='test3@email.com',
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
        assert len(json_data) == snippet_count

        # get the details of the snippet to be deleted
        detail_response = api_client.get(self.url + f"/{getattr(new_snippet, 'id')}")
        assert detail_response.status_code == 200
        details = detail_response.content.decode('utf-8')
        json_data = json.loads(details)
        assert json_data['tag'] == 'Test created tag'
        assert json_data['content'] == 'Test snippet creation.'
        assert json_data['owner'] == 'user_three'

        delete_response = api_client.delete(self.url+f"/{getattr(new_snippet, 'id')}")
        assert delete_response.status_code == 200
        list_of_items = delete_response.content.decode('utf-8')
        json_data = json.loads(list_of_items)
        assert len(json_data) == snippet_count - 1

        # get the details for the deleted snippets
        detail_response = api_client.get(self.url + f"/{getattr(new_snippet, 'id')}")
        assert detail_response.status_code == 404
        details = detail_response.content.decode('utf-8')
        json_data = json.loads(details)
        assert json_data['detail'] == 'Not found.'

    @pytest.mark.skipif(
        "TestSnippets.skip_all",
        reason="Model declaration error.",
    )
    def test_snippet_without_token(self, api_client_without_token):
        data = {
            "tag": {
                "title": "Snippet test tag"
            },
            "content": "This is content for the snippet test tag."
        }
        post_response = api_client_without_token.post(self.url, data, format='json')
        post_json_data = json.loads(post_response.content.decode('utf-8'))
        assert post_response.status_code == 401
        assert post_json_data['detail'] == "Authentication credentials were not provided."

        put_response = api_client_without_token.put(self.url, data, format='json')
        put_json_data = json.loads(put_response.content.decode('utf-8'))
        assert put_response.status_code == 401
        assert put_json_data['detail'] == "Authentication credentials were not provided."

        get_response = api_client_without_token.get(self.url)
        get_json_data = json.loads(get_response.content.decode('utf-8'))
        assert get_response.status_code == 401
        assert get_json_data['detail'] == "Authentication credentials were not provided."

        patch_response = api_client_without_token.patch(self.url, data, format='json')
        patch_json_data = json.loads(patch_response.content.decode('utf-8'))
        assert patch_response.status_code == 401
        assert patch_json_data['detail'] == "Authentication credentials were not provided."

        delete_response = api_client_without_token.delete(self.url)
        delete_json_data = json.loads(delete_response.content.decode('utf-8'))
        assert delete_response.status_code == 401
        assert delete_json_data['detail'] == "Authentication credentials were not provided."

    @pytest.mark.skipif(
        "TestSnippets.skip_all",
        reason="Model declaration error.",
    )
    def test_snippet_invalid_token(self, api_client_invalid_token):
        data = {
            "tag": {
                "title": "Snippet test tag"
            },
            "content": "This is content for the snippet test tag."
        }

        post_response = api_client_invalid_token.post(self.url, data, format='json')
        post_json_data = json.loads(post_response.content.decode('utf-8'))
        assert post_response.status_code == 401
        assert post_json_data['detail'] == "Authorization header must contain two space-delimited values"
        assert post_json_data['code'] == "bad_authorization_header"

        put_response = api_client_invalid_token.put(self.url, data, format='json')
        put_json_data = json.loads(put_response.content.decode('utf-8'))
        assert put_response.status_code == 401
        assert put_json_data['detail'] == "Authorization header must contain two space-delimited values"
        assert put_json_data['code'] == "bad_authorization_header"

        get_response = api_client_invalid_token.get(self.url)
        get_json_data = json.loads(get_response.content.decode('utf-8'))
        assert get_response.status_code == 401
        assert get_json_data['detail'] == "Authorization header must contain two space-delimited values"
        assert get_json_data['code'] == "bad_authorization_header"

        patch_response = api_client_invalid_token.patch(self.url, data, format='json')
        patch_json_data = json.loads(patch_response.content.decode('utf-8'))
        assert patch_response.status_code == 401
        assert patch_json_data['detail'] == "Authorization header must contain two space-delimited values"
        assert patch_json_data['code'] == "bad_authorization_header"

        delete_response = api_client_invalid_token.delete(self.url)
        delete_json_data = json.loads(delete_response.content.decode('utf-8'))
        assert delete_response.status_code == 401
        assert delete_json_data['detail'] == "Authorization header must contain two space-delimited values"
        assert delete_json_data['code'] == "bad_authorization_header"

