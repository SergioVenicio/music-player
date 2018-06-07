from . import models
from django import forms
from .utils import get_albuns
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm


class UsuarioAdmin(UserAdmin):
    model = models.Usuario
    fieldsets = (
        (None,
         {
            'fields': ('email', 'nome', 'sobrenome', 'avatar', 'password')
         }),
    )
    list_display = ('email', 'nome', 'sobrenome', 'is_staff')
    list_filter = ('email', 'nome', 'sobrenome',)
    search_fields = ('email', 'nome', 'sobrenome',)
    ordering = ('email', 'nome',)
    filter_horizontal = ('groups', 'user_permissions',)


class UsuarioForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': 'Email'}
        )
    )
    nome = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Nome'}
        )
    )
    sobrenome = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Sobrenome'}
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Senha'
            }
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Confirme sua senha'
            }
        )
    )
    avatar = forms.FileField(
        widget=forms.FileInput(
            attrs={'placeholder': 'Avatar'}
        )
    )

    class Meta:
        model = models.Usuario
        fields = (
            'email', 'nome', 'sobrenome', 'password1', 'password2', 'avatar'
        )


class MusicaForm(forms.ModelForm):
    nome = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Nome'}
        )
    )

    album = forms.ModelChoiceField(
        queryset=get_albuns(),
        widget=forms.Select(
            attrs={
                'class': 'form-control selectpicker', 'placeholder': 'Album',
                'data-live-search': 'true', 'data-style': 'btn-primary',
                'title': 'Escolha um album'
            })
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
