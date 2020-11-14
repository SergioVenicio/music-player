from rest_framework import serializers

from ..models import Music


class MusicSerializer(serializers.HyperlinkedModelSerializer):
    album = serializers.ReadOnlyField(source='album.name')
    file = serializers.CharField()

    class Meta:
        model = Music
        fields = (
            'id',
            'name',
            'album',
            'order',
            'file',
        )


class MusicSerializerList(serializers.HyperlinkedModelSerializer):
    album = serializers.ReadOnlyField(source='album.name')
    file = serializers.CharField()
    duration = serializers.CharField()

    class Meta:
        model = Music
        fields = (
            'id',
            'name',
            'album',
            'order',
            'file',
            'file_type',
            'duration'
        )
