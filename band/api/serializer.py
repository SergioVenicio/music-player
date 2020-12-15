from rest_framework import serializers

from ..models import Band, Genre


class GenreSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    genre_image = serializers.SerializerMethodField()

    def get_genre_image(self, genre):
        context = self.context.get('request')
        image_path = genre.get('genre_image')

        if image_path is None:
            return ''

        return context.build_absolute_uri(image_path)

    class Meta:
        model = Genre
        fields = (
            'id',
            'description',
            'genre_image'
        )


class BandSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    genre = serializers.ReadOnlyField(source='genre.description')
    band_image = serializers.SerializerMethodField()

    def get_band_image(self, band):
        image_path = band.get('band_image')

        if image_path is None:
            return ''

        context = self.context.get('request')
        return context.build_absolute_uri(image_path)

    class Meta:
        model = Band
        fields = (
            'id',
            'name',
            'genre',
            'band_image'
        )
