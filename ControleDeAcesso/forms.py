from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import PasswordChangeForm

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Nickname',widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Digite seu nick'}))
    password = forms.CharField(label='Senha',widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'Digite sua senha'}))

class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label='Senha antiga',widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(label='Nova senha',widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(label='Confirmar nova senha',widget=forms.PasswordInput(attrs={'class': 'form-control'}))