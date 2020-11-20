from rest_framework import serializers


from ..models import Album


class AlbumSerializer(serializers.HyperlinkedModelSerializer):
    cover_image = serializers.SerializerMethodField()
    band = serializers.ReadOnlyField(source='band.name')

    def get_cover_image(self, album):
        context = self.context.get('request')
        image_path = album['cover_image']
        return context.build_absolute_uri(image_path)

    class Meta:
        model = Album
        fields = (
            'id',
            'name',
            'band',
            'release_date',
            'cover_image',
        )
