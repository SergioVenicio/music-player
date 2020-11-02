from rest_framework import serializers

from album.models import Album
from band.models import Band, Genre
from music.models import Music
from user.models import User, Like


class GeneroSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('__all__')


class BandaSerializer(serializers.HyperlinkedModelSerializer):
    genre = serializers.ReadOnlyField(source='genre.description')

    class Meta:
        model = Band
        fields = ('__all__')


class AlbumSerializer(serializers.HyperlinkedModelSerializer):
    band = serializers.ReadOnlyField(source='band.name')

    class Meta:
        model = Album
        fields = ('__all__')


class MusicaSerializer(serializers.HyperlinkedModelSerializer):
    album = serializers.ReadOnlyField(source='album.name')

    class Meta:
        model = Music
        fields = ('name', 'album', 'order', 'file',)


class MusicaSerializerList(serializers.HyperlinkedModelSerializer):
    album = serializers.ReadOnlyField(source='album.name')

    class Meta:
        model = Music
        fields = (
            'id', 'name', 'album', 'order', 'file',
            'file_type', 'duration'
        )


class UsuarioSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'name', 'last_name', 'avatar')


class LikeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Like
        fields = ('__all__')


class LikeSerializerUsuario(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('__all__')


class LikeSerializerMusica(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('id', 'music', 'date',)
        depth = 1
