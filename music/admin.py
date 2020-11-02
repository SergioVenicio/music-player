from django.contrib import admin

from .models import Music


class MusicAdmin(admin.ModelAdmin):
    pass


admin.site.register(Music, MusicAdmin)
