from rest_framework import serializers

from ..models import Band, Genre


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('__all__')


class BandSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    genre = serializers.ReadOnlyField(source='genre.description')

    class Meta:
        model = Band
        fields = ('__all__')
