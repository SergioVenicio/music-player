from . import models
from django import forms
from .utils import get_albuns
from django.contrib.auth.admin import UserAdmin


class UsuarioAdmin(UserAdmin):
    model = models.Usuario
    fieldsets = (
        (None, {'fields': ('email', 'nome', 'sobrenome')}),
    )
    list_display = ('email', 'nome', 'sobrenome', 'is_staff')
    list_filter = ('email', 'nome', 'sobrenome',)
    search_fields = ('email', 'nome', 'sobrenome',)
    ordering = ('email', 'nome',)
    filter_horizontal = ('groups', 'user_permissions',)


class MusicaForm(forms.ModelForm):
    nome = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Nome'}
        )
    )

    album = forms.ModelChoiceField(
        queryset=get_albuns(),
        widget=forms.Select(
            attrs={'class': 'form-control', 'placeholder': 'Album'}
        )
    )

    ordem = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={'class': 'form-control', 'placeholder': 'Ordem'}
        )
    )

    arquivo = forms.FileField(
        widget=forms.FileInput(
            attrs={
                'class': 'form-control-file', 'placeholder': 'Arquivo'
            }
        )
    )

    class Meta:
        model = models.Musica
        exclude = ('arquivo_tipo', 'duracao',)
