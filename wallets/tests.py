# pylint: disable=import-error  disable=unused-argument  disable=too-few-public-methods
"""Importing test module"""
import pytest

from rest_framework.test import APIClient

from django.contrib.auth.models import User

pytestmark = pytest.mark.django_db
client = APIClient()


@pytest.mark.django_db
class TestUsers:
    """Creating test class for user model"""
    def test_my_user(self, create_user):
        """Creating test function for user model"""
        new_user = User.objects.get(username='user1')
        assert new_user.username == 'user1'
        assert new_user.id == 1
        assert new_user.password is not None


@pytest.mark.django_db
class TestApi:
    """Creating test class for API"""
    def test_new_user(self, create_user):
        """Testing user logging"""
        response = client.post("/api/login/", dict(username="user1", password="userpassword"))
        assert response.status_code == 403
