from django import forms
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm

from .models import User


class UserAdmin(UserAdmin):
    model = User
    fieldsets = (
        (None, {
            'fields': ('email', 'nome', 'sobrenome', 'avatar', 'password')
        }),
    )
    list_display = ('email', 'nome', 'sobrenome', 'is_staff')
    list_filter = ('email', 'nome', 'sobrenome',)
    search_fields = ('email', 'nome', 'sobrenome',)
    ordering = ('email', 'nome',)
    filter_horizontal = ('groups', 'user_permissions',)


class UserForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': 'Email'}
        )
    )
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Name'}
        )
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Last name'}
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Password'
            }
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Password confirmation'
            }
        )
    )
    avatar = forms.FileField(
        required=False,
        widget=forms.FileInput(
            attrs={'placeholder': 'Avatar'}
        )
    )

    class Meta:
        model = User
        fields = (
            'email',
            'name',
            'last_name',
            'password1',
            'password2',
            'avatar'
        )


class UserEditAvatar(forms.ModelForm):
    avatar = forms.FileField(
        required=False,
        widget=forms.FileInput(
            attrs={'placeholder': 'Avatar'}
        )
    )

    class Meta:
        model = User
        fields = ('avatar',)
