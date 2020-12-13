from django.contrib.auth.models import BaseUserManager

from . import models


class UserManager(BaseUserManager):
    use_in_migration = True

    def create_user(self, email, name, last_name, password, avatar=None):
        if not email:
            raise ValueError('The Email is required!')

        if not password:
            raise ValueError('The password is required!')
        elif len(password) < 6:
            raise ValueError('The password must be at least 6 characters!')

        user = models.User(
            email=self.normalize_email(email),
            name=name,
            last_name=last_name,
            avatar=avatar
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, name, last_name, password, avatar=None):
        user = self.create_user(
            email,
            name,
            last_name,
            password,
            avatar=avatar
        )
        user.is_admin = True
        user.save()
        return user
