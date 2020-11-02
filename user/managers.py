from django.contrib.auth.models import BaseUserManager

from . import models


class UserManager(BaseUserManager):
    use_in_migration = True

    def create_user(self, email, name, last_name, password, avatar=None):
        if not email:
            raise ValueError('O e-mail é obrigatorio!')

        if not password:
            raise ValueError('A senha é obrigatória!')
        elif len(password) < 6:
            raise ValueError('A senha deve ter pelo menos 6 caracteres!')

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
