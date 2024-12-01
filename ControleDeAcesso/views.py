from django.shortcuts import render
from .models import PolicialUsuario
from .forms import CustomPasswordChangeForm, LoginForm
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages

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

