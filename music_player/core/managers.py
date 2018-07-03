from music_player.core import models
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    """
        Classe de manipulação de usuários
    """
    use_in_migration = True

    def create_user(self, email, nome, sobrenome, password, avatar=None):
        """
            Cria um novo usuário
            :param email: String com email do usuário
            :param nome: String com o nome do usuário
            :param sobrenome: String com o sobrenome do usuário
            :param password: String com a senha do usuário
            :param avatar: Imagem do avatar do usuário
            :return: Uma instancia de usuário
        """
        if not email:
            raise ValueError('O e-mail é obrigatorio!')

        if not password:
            raise ValueError('A senha é obrigatória!')
        elif len(password) < 6:
            raise ValueError('A senha deve ter pelo menos 6 caracteres!')

        usuario = models.Usuario(
            email=self.normalize_email(email),
            nome=nome, sobrenome=sobrenome,
            avatar=avatar
        )
        usuario.set_password(password)
        usuario.save()
        return usuario

    def create_superuser(self, email, nome, sobrenome, password, avatar=None):
        """
            Cria um  usuário administrador
            :param email: String com email do usuário
            :param nome: String com o nome do usuário
            :param sobrenome: String com o sobrenome do usuário
            :param password: String com a senha do usuário
            :param avatar: Imagem do avatar do usuário
            :return: Uma instancia de usuário administrador
        """
        usuario = self.create_user(
            email, nome, sobrenome, password, avatar=avatar
        )
        usuario.is_admin = True
        usuario.save()
        return usuario
