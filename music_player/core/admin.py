from music_player.core import models, forms
from django.contrib import admin


admin.site.register(models.Genero)
admin.site.register(models.Banda)
admin.site.register(models.Album)
admin.site.register(models.Musica)
admin.site.register(models.Usuario, forms.UsuarioAdmin)
