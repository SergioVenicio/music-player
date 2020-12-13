import pytest

from django.db import IntegrityError

from user.models import User
from user.managers import UserManager


@pytest.mark.django_db(transaction=True)
class TestAlbum():
    def test_create(self):
        user = User(
            email='user_test@test.com',
            name='test',
            last_name='test',
            password='t&st321'
        )

        user.save()

        assert not user.is_admin

    def test_create_with_a_duplicated_email(self):
        user = User(
            email='user_test@test.com',
            name='test',
            last_name='test',
            password='t&st321'
        )
        other_user = User(
            email='user_test@test.com',
            name='test',
            last_name='test',
            password='t&st321'
        )

        user.save()
        with pytest.raises(IntegrityError):
            other_user.save()

    def test_manager_create(self):
        manager = UserManager()
        user = manager.create_user(
            email='user_test2@test.com',
            name='test',
            last_name='test',
            password='t&st321'
        )

        assert not user.is_admin

    def test_manager_create_super(self):
        manager = UserManager()
        user = manager.create_superuser(
            email='user_test3@test.com',
            name='test',
            last_name='test',
            password='t&st321'
        )

        assert user.is_admin
