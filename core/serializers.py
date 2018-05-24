from rest_framework import serializers
from core.models import Genero, Banda, Album, Musica


class GeneroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genero
        fields = ('__all__')


class BandaSerializer(serializers.HyperlinkedModelSerializer):
    genero = serializers.ReadOnlyField(source='genero.descricao')

    class Meta:
        model = Banda
        fields = ('__all__')


class AlbumSerializer(serializers.HyperlinkedModelSerializer):
    banda = serializers.ReadOnlyField(source='banda.nome')
    # capa = serializers.SerializerMethodField('get_path')

    def get_path(self, object):
        return f'http://localhost:8000/{object.capa.url}'

    class Meta:
        model = Album
        fields = ('__all__')


class MusicaSerializer(serializers.HyperlinkedModelSerializer):
    album = serializers.ReadOnlyField(source='album.nome')
    # arquivo = serializers.SerializerMethodField('get_path')

    def get_path(self, object):
        return f'http://localhost:8000/{object.arquivo.url}'

    def create(self, validated_data):
        return Musica(**validated_data)

    def validate(self, data):
        return data

    class Meta:
        model = Musica
        fields = ('nome', 'album', 'ordem', 'arquivo',)
