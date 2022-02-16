import pytest
from django.conf import settings
from authapp.models import User
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.fixture
def api_client():
    user = User.objects.create_user(username='user_one', email='test@email.com', password='test123')
    client = APIClient()
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    return client


@pytest.fixture
def api_client_without_token():
    client = APIClient()
    return client


@pytest.fixture
def api_client_invalid_token():
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer ')
    return client


@pytest.fixture()
def django_db_setup():
    settings.DATABASES["default"] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': settings.BASE_DIR / 'db.sqlite3',
    }
