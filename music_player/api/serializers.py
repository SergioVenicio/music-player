from music_player.core import models
from rest_framework import serializers


class GeneroSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Genero
        fields = ('__all__')


class BandaSerializer(serializers.HyperlinkedModelSerializer):
    genero = serializers.ReadOnlyField(source='genero.descricao')

    class Meta:
        model = models.Banda
        fields = ('__all__')


class AlbumSerializer(serializers.HyperlinkedModelSerializer):
    banda = serializers.ReadOnlyField(source='banda.nome')

    class Meta:
        model = models.Album
        fields = ('__all__')


class MusicaSerializer(serializers.HyperlinkedModelSerializer):
    album = serializers.ReadOnlyField(source='album.nome')

    class Meta:
        model = models.Musica
        fields = ('nome', 'album', 'ordem', 'arquivo',)


class MusicaSerializerList(serializers.HyperlinkedModelSerializer):
    album = serializers.ReadOnlyField(source='album.nome')

    class Meta:
        model = models.Musica
        fields = (
            'id', 'nome', 'album', 'ordem', 'arquivo',
            'arquivo_tipo', 'duracao'
        )


class UsuarioSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Usuario
        fields = ('id', 'email', 'nome', 'sobrenome', 'avatar')


class LikeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Like
        fields = ('__all__')


class LikeSerializerUsuario(serializers.ModelSerializer):
    class Meta:
        model = models.Like
        fields = ('__all__')


class LikeSerializerMusica(serializers.ModelSerializer):
    class Meta:
        model = models.Like
        fields = ('id', 'musica', 'data',)
        depth = 1
