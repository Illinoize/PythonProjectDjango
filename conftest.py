# pylint: disable=import-error  disable=redefined-outer-name
"""Importing modules to prepare data for tests"""
import pytest

from django.contrib.auth.models import User


@pytest.fixture(scope='function')
def create_user():
    """Creating an user instance"""
    user1 = User.objects.create(
        username='user1',
        password='userpassword'
    )
    user2 = User.objects.create(
        username='user2',
        password='newpassword'
    )
    return user1, user2
