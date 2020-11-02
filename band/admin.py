from django.contrib import admin

from .models import Band, Genre


class BandAdmin(admin.ModelAdmin):
    pass


class GenreAdmin(admin.ModelAdmin):
    pass


admin.site.register(Band, BandAdmin)
admin.site.register(Genre, GenreAdmin)
