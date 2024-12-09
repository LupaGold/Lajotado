from django.shortcuts import render
from .models import PolicialUsuario
from .forms import CustomPasswordChangeForm, LoginForm, CadastroForm
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
import random
import string
import requests
from django.views.generic import TemplateView, ListView, DetailView, View, CreateView, UpdateView
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
import json

class AlterarSenhaView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'Form.html'  
    success_url = reverse_lazy('AlterarSenha')  
    form_class = CustomPasswordChangeForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['players_data'] =  PolicialUsuario.objects.filter(username=self.request.user)
        context["titulo"] = 'Alterar Senha'
        context["image"] = 'cadeado.gif'
        context["descricao"] = 'Uma senha segura envita acessos indesejados em sua conta!'
        return context

class LoginViewModificada(LoginView):
    template_name = 'Login.html'
    authentication_form = LoginForm

class CadastroView(TemplateView):
    template_name = 'Cadastro.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        codigo_aleatorio = self.GerarCódigo()
        context['form'] = CadastroForm()
        context['codigo_aleatorio'] = codigo_aleatorio
        return context
    
    def get(self, request):
        codigo_aleatorio = self.GerarCódigo()
        request.session['codigo_aleatorio'] = codigo_aleatorio  # Armazena o código na sessão
        form = CadastroForm(initial={'codigo_aleatorio': codigo_aleatorio})
        return render(request, self.template_name, {'form': form, 'codigo_aleatorio': codigo_aleatorio})

    def post(self, request, *args, **kwargs):
        form = CadastroForm(request.POST)
        codigo_aleatorio = request.session.get('codigo_aleatorio')  # Recupera da sessão
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            if self.CheckarCódigo(username, codigo_aleatorio):
                self.AlterarSenha(username, password)
                return redirect('Login')
            elif not self.CheckarUsuario(username):
                form.add_error(None, 'Policial não registrado!')
            else:
                form.add_error(None, 'Código aleatório inválido')
        return render(request, self.template_name, {'form': form, 'codigo_aleatorio': codigo_aleatorio})

    
    def GerarCódigo(self):
        letters = string.ascii_uppercase
        digits = ''.join(random.choice(string.digits) for _ in range(3))
        return 'RHC' + digits
    
    def CheckarUsuario(self, username):
        return PolicialUsuario.objects.filter(username=username).exists()

    def CheckarCódigo(self, username, codigo_aleatorio):
        try:
            response = requests.get(f'https://www.habbo.com.br/api/public/users?name={username}')
            print(f'https://www.habbo.com.br/api/public/users?name={username}')
            print(f"Status da Resposta: {response.status_code}")
            print(f"Conteúdo da Resposta: {response.text}")
            if response.status_code == 200:
                data = response.json()
                motto = data.get('motto').strip()
                print('Código aleatório:', codigo_aleatorio)
                print('Código aleatório da API:', motto)
                if codigo_aleatorio == motto:
                    return True
                else:
                    return False
            else:
                print(f"Erro na API: Status {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"Erro ao acessar a API: {e}")
            return False
        
    def AlterarSenha(self, username, password):
        user = PolicialUsuario.objects.get(username=username)
        user.set_password(password)
        user.save()
