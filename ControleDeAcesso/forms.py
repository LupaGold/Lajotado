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

class CadastroForm(forms.Form):
    username = forms.CharField(label='Nick:', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Digite seu nick'}))
    password = forms.CharField(label='Senha', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'Digite sua senha'}))
    confirm_password = forms.CharField(label='Confirme a senha', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'Confirme sua senha'}))
    codigo_aleatorio = forms.CharField(widget=forms.HiddenInput(),required=False)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("As senhas não coincidem. Por favor, digite novamente.")

        return cleaned_data