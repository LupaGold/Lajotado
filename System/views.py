from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView, View, CreateView, UpdateView
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.urls import reverse
from braces.views import GroupRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormMixin
from .models import (Post, JA, LogJA, EmblemaCompra, EmblemasModel, PostagemJornal, 
                     LogPostagem, Treinamentos, LogTreinamento, RelatorioTreinamento,
                     LogDocumentos, Documentos, Requerimento, LogRequerimento, LogTimeLine, PROMOCAO, LogStaff, Destaques)
from .forms import (PostForm, ComentarioForm, JAForm, PostagemForm, 
TreinamentosForm, RelatorioForm, DocumentosForm, RequerimentoForm, RequerimentoContratoForm, DestaqueForm)
from ControleDeAcesso.models import PolicialUsuario, CARGOS
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.models import Group, User
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.db.models import Count
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
class PainelPrincipal(LoginRequiredMixin,TemplateView,FormMixin):
    template_name = 'Principal.html'
    model = Post
    context_object_name = 'posts'
    form_class = PostForm
    comentario_form_class = ComentarioForm

    def post(self, request, *args, **kwargs):
        if 'post_id' in request.POST:  # Identifica o formulário de comentário
            comentario_form = self.comentario_form_class(request.POST)
            if comentario_form.is_valid():
                comentario_form.instance.autor = self.request.user
                comentario_form.instance.post_id = request.POST.get('post_id')
                comentario_form.save()
                return HttpResponseRedirect(self.get_success_url())
            else:
                return self.form_invalid(comentario_form)
        else:
            form = self.get_form()
            if form.is_valid():
                form.instance.autor = self.request.user
                form.save()
                return HttpResponseRedirect(self.get_success_url())
            else:
                return self.form_invalid(form)

    def get_success_url(self):
        return reverse('PainelPrincipal')
    
    def get(self, request, *args, **kwargs):
        search_term = request.GET.get('search', '') 
        policial = PolicialUsuario.objects.filter(username__icontains=search_term) if search_term else None

        context = {
            'form': self.get_form(),
            'posts': Post.objects.all().order_by('-data'),
            'comentario_form': self.comentario_form_class(),
            'policial': policial,
            'busca': search_term,
            'alistados': PolicialUsuario.objects.order_by('-id')[:5],
            'emblema': EmblemasModel.objects.last(),
            'destaques': Destaques.objects.last(),
        }
        return self.render_to_response(context)
    
class MeusAvais(LoginRequiredMixin, TemplateView):
    model = JA
    template_name = 'MeusAvais.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['avais'] = JA.objects.filter(solicitante=self.request.user).order_by('-datatime')
        return context
    
class RegistrarAval(LoginRequiredMixin, CreateView):
    form_class = JAForm
    template_name = 'Form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = 'Registrar Licença'
        context["image"] = 'relatorio.png'
        context["descricao"] = 'Verifique todos os campos antes de registrar a Licença!'
        return context
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.instance.solicitante = self.request.user
            new_ja = form.save()
            
            log = LogJA.objects.create(
                    aval=new_ja,
                    texto=f"{new_ja.solicitante} registrou uma licença!",
                    datatime=timezone.now(),
                )

            log.save()
            messages.success(request, f'Licença solicitada!')
            return HttpResponseRedirect(reverse('MeusAvais'))
        else:
            return self.get(request, *args, **kwargs)
        
class AvaisGeral(GroupRequiredMixin, ListView):
    model = JA
    template_name = 'AvaisGeral.html'
    context_object_name = 'avais'
    group_required = [u'STAFF', u'Analista', u'LDRH']

    def get_queryset(self):
        q = self.request.GET.get('q')
        queryset = JA.objects.all()

        if q:
            queryset = queryset.filter(solicitante__username__icontains=q)

        queryset = queryset.order_by('-datatime')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total'] = JA.objects.all().count()
        return context
    
class AprovarAvalView(GroupRequiredMixin, View):
    group_required = [u'STAFF', u'Analista', u'LDRH']

    def post(self, request, *args, **kwargs):
        ja_id = kwargs.get('ja_id')
        ja = get_object_or_404(JA, id=ja_id)
        ja.status = 'Aprovado'
        ja.save()

        LogJA.objects.create(
            aval=ja,
            texto=f'A licença solicitada por {ja.solicitante.patente} {ja.solicitante.username} foi aprovado por {request.user.username}.',
            datatime=timezone.now()
        )
        messages.success(request, f'Licença aprovada!')

        return HttpResponseRedirect(reverse('GeralAvais'))

class RejeitarAvalView(GroupRequiredMixin, View):
    group_required = [u'STAFF', u'Analista', u'LDRH']

    def post(self, request, *args, **kwargs):
        ja_id = kwargs.get('ja_id')
        ja = get_object_or_404(JA, id=ja_id)
        ja.status = 'Reprovado'
        ja.save()

        LogJA.objects.create(
            aval=ja,
            texto=f'A licença solicitada por {ja.solicitante.patente} {ja.solicitante.username} foi rejeitado por {request.user.username}.',
            datatime=timezone.now()
        )
        messages.success(request, f'Licença rejeitada!')
        return HttpResponseRedirect(reverse('GeralAvais'))

class LojaEmblemasView(LoginRequiredMixin, TemplateView):

    template_name = 'Loja.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        emblemas = EmblemasModel.objects.all().order_by('-datatime')
        emblemas_comprados = EmblemaCompra.objects.filter(solicitante=self.request.user).values_list('emblema_id', flat=True)
        context['emblemas'] = emblemas
        context['emblemas_comprados'] = emblemas_comprados
        context['total'] = EmblemasModel.objects.all().count()
        return context

class ComprarEmblemaView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        emblema_id = kwargs.get('emblema_id')
        emblema = get_object_or_404(EmblemasModel, id=emblema_id)
        usuario = request.user

        # Verifica se o usuário já tem o emblema
        if EmblemaCompra.objects.filter(solicitante=usuario, emblema=emblema).exists():
            messages.error(request, 'Você já comprou este emblema.')
            return redirect(reverse('Loja'))

        # Verifica se o usuário tem moedas
        if usuario.moedas < emblema.moedas:
            messages.error(request, 'Você não tem moedas suficientes para comprar este emblema.')
            return redirect(reverse('Loja'))

        with transaction.atomic():
            # Deduz o coin do usuário
            usuario.moedas -= emblema.moedas
            usuario.save()

            # Cria a compra do emblema
            EmblemaCompra.objects.create(solicitante=usuario, emblema=emblema)

        messages.success(request, 'Emblema comprado com sucesso!')
        return redirect(reverse('Loja'))

class JornalPrincipal(LoginRequiredMixin, TemplateView):
    template_name = 'PrincipalJornal.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #Grupo de Jornalista 
        membro = 'Jornalista'
        #Lógica para testar os Militares se fazem parte dos grupos
        try:
            grupo_membro = Group.objects.get(name=membro)
            context['membros'] = PolicialUsuario.objects.filter(groups=grupo_membro).order_by('patente_order')
        except Group.DoesNotExist:
            context['membros'] = PolicialUsuario.objects.none()

        context["postagens"] = PostagemJornal.objects.all().order_by('-datatime')
        context["emblema"] = EmblemasModel.objects.last()
        context["alistados"] = PolicialUsuario.objects.order_by('-id')[:5]
        return context
    
class Postagens(LoginRequiredMixin, DetailView):
    model = PostagemJornal
    template_name = 'PostagensJornal.html'
    context_object_name = 'postagem'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["emblema"] = EmblemasModel.objects.last()
        context["alistados"] = PolicialUsuario.objects.order_by('-id')[:5]
        return context
    
class RegistrarPostagem(GroupRequiredMixin, CreateView):
    model = PostagemJornal
    template_name = 'Form.html'
    form_class = PostagemForm
    group_required = [u'STAFF', u'Jornalista', u'EDC']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = 'Publicar matéria'
        context["image"] = 'jornal.png'
        context["descricao"] = 'Verifique todos os campos antes de publicar a matéria!'
        return context
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.instance.solicitante = self.request.user
            form.instance.datatime = timezone.now()
            new = form.save()

            try:
                log = LogPostagem.objects.create(
                    treinamento=new,
                    texto=f"{new.solicitante} publicou uma matéria!",
                    datatime=timezone.now(),
                )
                log.save()
                messages.success(request, f'Postagem registrada!')
            except Exception as e:
                print(f"Erro ao salvar o log: {e}")

            return HttpResponseRedirect(reverse('Jornal'))
        else:
            return self.form_invalid(form)
        
class EditarPostagem(GroupRequiredMixin, UpdateView):
    model = PostagemJornal
    template_name = 'Form.html'
    form_class = PostagemForm
    group_required = [u'STAFF', u'Jornalista', u'EDC']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = 'Editar matéria'
        context["image"] = 'jornal.png'
        context["descricao"] = 'Verifique todos os campos antes de editar a matéria!'
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            form.instance.solicitante = self.request.user
            form.instance.datatime = timezone.now()
            new = form.save()

            try:
                log = LogPostagem.objects.create(
                    treinamento=new,
                    texto=f"{new.solicitante} editou a matéria {new.titulo}!",
                    datatime=timezone.now(),
                )
                log.save()
                messages.success(request, f'Postagem editada!')
            except Exception as e:
                print(f"Erro ao salvar o log: {e}")

            return HttpResponseRedirect(reverse('Jornal'))
        else:
            return self.form_invalid(form)
        
class Jornalistas(GroupRequiredMixin, ListView):
    template_name = 'Jornalistas.html'
    model = PolicialUsuario
    context_object_name = 'policiais'
    group_required = [u'STAFF', u'EDC']
    
    def get_queryset(self):
        q = self.request.GET.get('q')
        grupo_membro = Group.objects.get(name='Jornalista')
        queryset = PolicialUsuario.objects.exclude(groups=grupo_membro).order_by('patente_order')

        if q:
            queryset = queryset.filter(username__icontains=q)

        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #Grupo de Jornalista 
        membro = 'Jornalista'
        #Lógica para testar os Militares se fazem parte dos grupos
        try:
            grupo_membro = Group.objects.get(name=membro)
            context['membros'] = PolicialUsuario.objects.filter(groups=grupo_membro).order_by('patente_order')
        except Group.DoesNotExist:
            context['membros'] = PolicialUsuario.objects.none()
        return context
    
@method_decorator(csrf_protect, name='dispatch')
class AdicionarJornalista(GroupRequiredMixin, View):
    template_name = 'Form.html'
    group_required = [u'STAFF', u'EDC']
    def post(self, request, user_id):
        user = get_object_or_404(PolicialUsuario, id=user_id)
        group = Group.objects.get(name='Jornalista')
        user.groups.add(group)
        log = LogPostagem.objects.create(
                    texto=f"{self.request.user} nomeou {user.username} como Jornalista!",
                    datatime=timezone.now(),
                )
        log.save()
        messages.success(request, f'Você nomeou {user.username} como Jornalista!')
        return redirect('Jornalistas')

@method_decorator(csrf_protect, name='dispatch')
class RemoverJornalista(GroupRequiredMixin, View):
    template_name = 'Form.html'
    group_required = [u'STAFF', u'EDC']
    def post(self, request, user_id):
        user = get_object_or_404(PolicialUsuario, id=user_id)
        group = Group.objects.get(name='Jornalista')
        user.groups.remove(group)
        log = LogPostagem.objects.create(
                    texto=f"{self.request.user} exonerou {user.username} como Jornalista!",
                    datatime=timezone.now(),
                )
        log.save()
        messages.success(request, f'Você exonerou {user.username} como Jornalista!')
        return redirect('Jornalistas')
    
class TreinamentosView(LoginRequiredMixin,ListView):
    model = Treinamentos
    template_name = 'Treinamentos.html'
    context_object_name = 'treinamentos'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["alistados"] = PolicialUsuario.objects.order_by('-id')[:5]
        return context

class EditarTreinamento(GroupRequiredMixin, UpdateView):
    model = Treinamentos
    template_name = 'Form.html'
    form_class = TreinamentosForm
    group_required = [u'STAFF', u'LDPE']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = 'Editar Treinamento'
        context["image"] = 'bolsa2.gif'
        context["descricao"] = 'Verifique todos os campos antes de editar o treinamento!'
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            form.instance.solicitante = self.request.user
            form.instance.datatime = timezone.now()
            new = form.save()

            try:
                log = LogTreinamento.objects.create(
                    treinamento=new,
                    texto=f"{new.solicitante} editou o treinamento {new.titulo}",
                    datatime=timezone.now(),
                )
                log.save()
                messages.success(request, f'Treinamento editado!')
            except Exception as e:
                print(f"Erro ao salvar o log: {e}")

            return HttpResponseRedirect(reverse('Treinamentos'))
        else:
            return self.form_invalid(form)
    
class RegistrarTreinamento(GroupRequiredMixin, CreateView):
    model = Treinamentos
    template_name = 'Form.html'
    form_class = TreinamentosForm
    group_required = [u'STAFF', u'LDPE']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = 'Registrar Treinamento'
        context["image"] = 'bolsa2.gif'
        context["descricao"] = 'Verifique todos os campos antes de publicar o treinamento!'
        return context
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.instance.solicitante = self.request.user
            form.instance.datatime = timezone.now()
            new = form.save()

            try:
                log = LogTreinamento.objects.create(
                    treinamento=new,
                    texto=f"{new.solicitante} registrou um treinamento!",
                    datatime=timezone.now(),
                )
                log.save()
                messages.success(request, f'Treinamento registrado!')
            except Exception as e:
                print(f"Erro ao salvar o log: {e}")

            return HttpResponseRedirect(reverse('Treinamentos'))
        else:
            return self.form_invalid(form)
        
class RelatoriosTreinamentos(GroupRequiredMixin, TemplateView):
    model = RelatorioTreinamento
    template_name = 'Relatorios.html'
    group_required = [u'STAFF', u'LDPE', u'GUIADpE', u'MinistroDpE']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["alistados"] = PolicialUsuario.objects.order_by('-id')[:5]
        context['relatorios'] = RelatorioTreinamento.objects.filter(solicitante=self.request.user).order_by('-datatime')
        context['contador'] = RelatorioTreinamento.objects.filter(solicitante=self.request.user).values('treinamento__titulo').annotate(total=Count('treinamento'))
        context['total'] = RelatorioTreinamento.objects.filter(solicitante=self.request.user).count()
        return context
    
class RegistrarRelatorioTreinamento(GroupRequiredMixin, CreateView):
    model = RelatorioTreinamento
    template_name = 'Form.html'
    form_class = RelatorioForm
    group_required = [u'STAFF', u'LDPE', u'GUIADpE', u'MinistroDpE']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = 'Registrar Relatório'
        context["image"] = 'relatorio.png'
        context["descricao"] = 'Verifique todos os campos antes de registrar o relatório!'
        return context
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.instance.solicitante = self.request.user
            form.instance.datatime = timezone.now()
            new = form.save()

            try:
                log = LogTreinamento.objects.create(
                    texto=f"{new.solicitante} enviou um relatório de treinamento",
                    datatime=timezone.now(),
                )
                log.save()
                messages.success(request, f'Relatório registrado!')
            except Exception as e:
                print(f"Erro ao salvar o log: {e}")

            return HttpResponseRedirect(reverse('RelatoriosTreinamentos'))
        else:
            return self.form_invalid(form)
        
class RelatorioGeral(GroupRequiredMixin, ListView):
    model = RelatorioTreinamento
    template_name = 'RelatoriosGeral.html'
    context_object_name = 'relatorios'
    group_required = [u'STAFF', u'LDPE', u'MinistroDpE']

    def get_queryset(self):
        q = self.request.GET.get('q')
        queryset = RelatorioTreinamento.objects.all()

        if q:
            queryset = queryset.filter(solicitante__username__icontains=q)

        queryset = queryset.order_by('-datatime')

        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ranking = RelatorioTreinamento.objects.all().values('solicitante__username').annotate(total=Count('id')).order_by('-total')
        context['contador'] = RelatorioTreinamento.objects.all().values('treinamento__titulo').annotate(total=Count('treinamento'))
        context['total'] = RelatorioTreinamento.objects.all().count()
        context['ranking'] = ranking
        return context
    
class AprovarRelatorio(GroupRequiredMixin, View):
    group_required = [u'STAFF', u'LDPE', u'MinistroDpE']
    def post(self, request, *args, **kwargs):
        # Obtém o ID do relatório da URL
        relatorio_id = kwargs.get('relatorio_id')
        relatorio = get_object_or_404(RelatorioTreinamento, id=relatorio_id)

        # Alterando o status do relatório para 'Aprovado'
        relatorio.status = 'Aprovado'
        relatorio.save()
        # Verificando se o relatório está relacionado ao treinamento "Curso de Formação de Agentes"
        if relatorio.treinamento.titulo == "Curso de Formação de Agentes":
            aprovado_username = relatorio.aprovado.strip()  # Supondo que 'aprovado' seja o campo com o nome de usuário

            if aprovado_username:
                User = get_user_model()
                try:
                    # Tenta encontrar um usuário com o username fornecido
                    aprovado_user = User.objects.get(username=aprovado_username)
                except User.DoesNotExist:
                    # Se o usuário não existir, cria um novo usuário
                    aprovado_user = User.objects.create_user(
                        username=aprovado_username,
                        password='fauiuaufauj20981428042',  # Defina uma senha padrão ou gere uma
                        patente='Agente',
                    )
        log0 = LogTimeLine.objects.create(
                            policial=relatorio.aprovado,
                            texto=f"O policial {relatorio.aprovado} ingressou na RHC!",
                            datatime=timezone.now(),
                            requerimento='Ingresso'
                        )
        log0.save()
        # Criando o log de aprovação
        log = LogTimeLine.objects.create(
                            policial=relatorio.aprovado,
                            texto=f"O policial {relatorio.aprovado} foi aprovado no {relatorio.treinamento.titulo} pelo instrutor {relatorio.solicitante.username}. Observações: {relatorio.obs}",
                            datatime=timezone.now(),
                            requerimento='Treinamento'
                        )
        log.save()
        LogTreinamento.objects.create(
            texto=f'O Relatório de treinamento enviado por {relatorio.solicitante.patente} {relatorio.solicitante.username} foi aprovado por {request.user.username}.',
            datatime=timezone.now()
        )
        messages.success(request, f'Relatório aprovado!')
        # Redirecionando para a página de relatórios gerais
        return HttpResponseRedirect(reverse('RelatoriosGeral'))
    
class ReprovarRelatorio(GroupRequiredMixin, View):
    group_required = [u'STAFF', u'LDPE', u'MinistroDpE']
    def post(self, request, *args, **kwargs):
        relatorio_id = kwargs.get('relatorio_id')
        relatorio = get_object_or_404(RelatorioTreinamento, id=relatorio_id)
        relatorio.status = 'Reprovado'
        relatorio.save()
        LogTreinamento.objects.create(
            texto=f'O Relatório de treinamento enviado por {relatorio.solicitante.patente} {relatorio.solicitante.username} foi reprovado por {request.user.username}.',
            datatime=timezone.now()
        )
        messages.success(request, f'Relatório reprovado!')
        return HttpResponseRedirect(reverse('RelatoriosGeral'))
    
@method_decorator(csrf_protect, name='dispatch')
class AdicionarGuia(GroupRequiredMixin, View):
    group_required = [u'STAFF', u'LDPE', u'MinistroDpE']
    template_name = 'Form.html'
    def post(self, request, user_id):
        user = get_object_or_404(PolicialUsuario, id=user_id)
        group = Group.objects.get(name='GuiaDpE')
        user.groups.add(group)
        log = LogTreinamento.objects.create(
                    texto=f"{self.request.user} nomeou {user.username} como Guia do Departamento Educacional!",
                    datatime=timezone.now(),
                )
        log.save()
        messages.success(request, f'Você nomeou {user.username} como Guia do Departamento Educacional!')
        return redirect('Guias')

@method_decorator(csrf_protect, name='dispatch')
class RemoverGuia(GroupRequiredMixin, View):
    group_required = [u'STAFF', u'LDPE', u'MinistroDpE']
    template_name = 'Form.html'
    def post(self, request, user_id):
        user = get_object_or_404(PolicialUsuario, id=user_id)
        group = Group.objects.get(name='GuiaDpE')
        user.groups.remove(group)
        log = LogTreinamento.objects.create(
                    texto=f"{self.request.user} exonerou {user.username} como Guia do Departamento Educacional!",
                    datatime=timezone.now(),
                )
        log.save()
        messages.success(request, f'Você exonerou {user.username} como Guia do Departamento Educacional!')
        return redirect('Guias')
    
@method_decorator(csrf_protect, name='dispatch')
class AdicionarMinistroDpE(GroupRequiredMixin, View):
    group_required = [u'STAFF', u'LDPE']
    template_name = 'Form.html'
    def post(self, request, user_id):
        user = get_object_or_404(PolicialUsuario, id=user_id)
        group = Group.objects.get(name='MinistroDpE')
        user.groups.add(group)
        log = LogTreinamento.objects.create(
                    texto=f"{self.request.user} nomeou {user.username} como Ministro do Departamento Educacional!",
                    datatime=timezone.now(),
                )
        log.save()
        messages.success(request, f'Você nomeou {user.username} como Ministro do Departamento Educacional!')
        return redirect('MinistroDpE')

@method_decorator(csrf_protect, name='dispatch')
class RemoverMinistroDpE(GroupRequiredMixin, View):
    group_required = [u'STAFF', u'LDPE']
    template_name = 'Form.html'
    def post(self, request, user_id):
        user = get_object_or_404(PolicialUsuario, id=user_id)
        group = Group.objects.get(name='MinistroDpE')
        user.groups.remove(group)
        log = LogTreinamento.objects.create(
                    texto=f"{self.request.user} exonerou {user.username} como Ministro do Departamento Educacional!",
                    datatime=timezone.now(),
                )
        log.save()
        messages.success(request, f'Você exonerou {user.username} como Ministro do Departamento Educacional!')
        return redirect('MinistroDpE')
    
class GuiasDpEView(GroupRequiredMixin, ListView):
    group_required = [u'STAFF', u'LDPE', u'MinistroDpE']
    template_name = 'GuiaDpE.html'
    model = PolicialUsuario
    context_object_name = 'policiais'
    
    def get_queryset(self):
        q = self.request.GET.get('q')
        grupo_membro = Group.objects.get(name='GuiaDpE')
        queryset = PolicialUsuario.objects.exclude(groups=grupo_membro).order_by('patente_order')

        if q:
            queryset = queryset.filter(username__icontains=q)

        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #Grupo de Jornalista 
        membro = 'GuiaDpE'
        #Lógica para testar os Militares se fazem parte dos grupos
        try:
            grupo_membro = Group.objects.get(name=membro)
            context['membros'] = PolicialUsuario.objects.filter(groups=grupo_membro).order_by('patente_order')
        except Group.DoesNotExist:
            context['membros'] = PolicialUsuario.objects.none()
        return context
    
class MinistroDpEView(GroupRequiredMixin, ListView):
    group_required = [u'STAFF', u'LDPE']
    template_name = 'MinistroDpE.html'
    model = PolicialUsuario
    context_object_name = 'policiais'
    
    def get_queryset(self):
        q = self.request.GET.get('q')
        grupo_membro = Group.objects.get(name='MinistroDpE')
        queryset = PolicialUsuario.objects.exclude(groups=grupo_membro).order_by('patente_order')

        if q:
            queryset = queryset.filter(username__icontains=q)

        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #Grupo de Jornalista 
        membro = 'MinistroDpE'
        #Lógica para testar os Militares se fazem parte dos grupos
        try:
            grupo_membro = Group.objects.get(name=membro)
            context['membros'] = PolicialUsuario.objects.filter(groups=grupo_membro).order_by('patente_order')
        except Group.DoesNotExist:
            context['membros'] = PolicialUsuario.objects.none()
        return context
    
class DocumentosView(LoginRequiredMixin, ListView):
    model = Documentos
    template_name = 'Documentos.html'
    context_object_name = 'Documentos'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["alistados"] = PolicialUsuario.objects.order_by('-id')[:5]
        return context

class EditarDocumentos(GroupRequiredMixin, UpdateView):
    group_required = [u'STAFF']
    model = Documentos
    template_name = 'Form.html'
    form_class = DocumentosForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = 'Editar Documento'
        context["image"] = 'bolsa2.gif'
        context["descricao"] = 'Verifique todos os campos antes de editar o Documento!'
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            form.instance.solicitante = self.request.user
            form.instance.datatime = timezone.now()
            new = form.save()

            try:
                log = LogDocumentos.objects.create(
                    treinamento=new,
                    texto=f"{new.solicitante} editou o documento {new.titulo}",
                    datatime=timezone.now(),
                )
                log.save()
                messages.success(request, f'Documento editado!')
            except Exception as e:
                print(f"Erro ao salvar o log: {e}")

            return HttpResponseRedirect(reverse('Documentos'))
        else:
            return self.form_invalid(form)
    
class RegistrarDocumento(GroupRequiredMixin, CreateView):
    model = Documentos
    template_name = 'Form.html'
    form_class = DocumentosForm
    group_required = [u'STAFF']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = 'Registrar Documento'
        context["image"] = 'bolsa2.gif'
        context["descricao"] = 'Verifique todos os campos antes de publicar o Documento!'
        return context
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.instance.solicitante = self.request.user
            form.instance.datatime = timezone.now()
            new = form.save()

            try:
                log = LogDocumentos.objects.create(
                    treinamento=new,
                    texto=f"{new.solicitante} registrou o documento {new.titulo}!",
                    datatime=timezone.now(),
                )
                log.save()
                messages.success(request, f'Documento registrado!')
            except Exception as e:
                print(f"Erro ao salvar o log: {e}")

            return HttpResponseRedirect(reverse('Documentos'))
        else:
            return self.form_invalid(form)
        
class RegistrarRequerimento(GroupRequiredMixin, CreateView):
    model = Requerimento
    template_name = 'Form.html'
    form_class = RequerimentoForm
    group_required = [u'STAFF', u'Analista', u'LDRH']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = 'Registrar Requerimento'
        context["image"] = 'relatorio.png'
        context["descricao"] = 'Verifique todos os campos antes de registrar o requerimento!'
        return context
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.instance.solicitante = self.request.user
            form.instance.datatime = timezone.now()
            new = form.save()

            try:
                log = LogRequerimento.objects.create(
                    requerimento=new,
                    texto=f"{new.solicitante} enviou um requerimento de {new.requerimento}",
                    datatime=timezone.now(),
                )
                log.save()
                messages.success(request, f'Requerimento registrado!')
            except Exception as e:
                print(f"Erro ao salvar o log: {e}")

            return HttpResponseRedirect(reverse('Requerimentos'))
        else:
            return self.form_invalid(form)
        
class Requerimentos(GroupRequiredMixin, ListView):
    model = Requerimento
    template_name = 'Requerimentos.html'
    context_object_name = 'relatorios'
    group_required = [u'STAFF', u'Analista', u'LDRH']

    def get_queryset(self):
        q = self.request.GET.get('q')
        queryset = Requerimento.objects.all()

        if q:
            queryset = queryset.filter(solicitante__username__icontains=q)

        queryset = queryset.order_by('-datatime')

        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contador'] = Requerimento.objects.all().values('requerimento').annotate(total=Count('requerimento'))
        context['total'] = Requerimento.objects.all().count()
        return context

class ReprovarRequerimento(GroupRequiredMixin, View):
    group_required = [u'STAFF', u'Analista', u'LDRH']
    def post(self, request, *args, **kwargs):
        relatorio_id = kwargs.get('relatorio_id')
        relatorio = get_object_or_404(Requerimento, id=relatorio_id)
        relatorio.status = 'Reprovado'
        relatorio.save()
        LogRequerimento.objects.create(
            requerimento=relatorio,
            texto=f'O requerimento de {relatorio.requerimento} enviado por {relatorio.solicitante.patente} {relatorio.solicitante.username} foi reprovado por {request.user.username}.',
            datatime=timezone.now()
        )
        messages.success(request, f'Requerimento reprovado!')
        return HttpResponseRedirect(reverse('Requerimentos'))

class AprovarRequerimento(GroupRequiredMixin, View):
    group_required = [u'STAFF', u'Analista', u'LDRH']
    @method_decorator(csrf_protect)
    def post(self, request, *args, **kwargs):
        # Obtém o ID do relatório da URL
        relatorio_id = kwargs.get('relatorio_id')
        relatorio = get_object_or_404(Requerimento, id=relatorio_id)
        User = get_user_model()
        policial = relatorio.policial.strip()
        if relatorio.requerimento == "Promoção":
            try:
                requerimento_user = User.objects.get(username=policial)
                patente_atual = requerimento_user.patente
                proxima_patente = PROMOCAO.get(patente_atual)
                requerimento_user.patente = proxima_patente
                requerimento_user.save()
                LogRequerimento.objects.create(
                requerimento=relatorio,
                texto=f'O requerimento de {relatorio.requerimento} enviado por {relatorio.solicitante.patente} {relatorio.solicitante.username} foi aprovado por {request.user.username}.',
                datatime=timezone.now()
                )
                log = LogTimeLine.objects.create(
                                policial=relatorio.policial,
                                texto=f"Foi promovido para o cargo de {proxima_patente}. Motivo: {relatorio.obs}",
                                datatime=timezone.now(),
                                requerimento='Promoção'
                            )
                log.save()
                relatorio.status = 'Aprovado'
                relatorio.save()
            except User.DoesNotExist:
                messages.error(request, f"O policial com o username '{relatorio.policial}' não foi encontrado. Não é possível realizar a promoção.")
        
        elif relatorio.requerimento == "Rebaixamento":
            try:
                requerimento_user = User.objects.get(username=policial)
                patente_atual = requerimento_user.patente
                patentes_ordenadas = [patente[0] for patente in CARGOS]
                indice_atual = patentes_ordenadas.index(patente_atual)
                proxima_patente = patentes_ordenadas[indice_atual - 1]
                requerimento_user.patente = proxima_patente
                requerimento_user.save()
                LogRequerimento.objects.create(
                requerimento=relatorio,
                texto=f'O requerimento de {relatorio.requerimento} enviado por {relatorio.solicitante.patente} {relatorio.solicitante.username} foi aprovado por {request.user.username}.',
                datatime=timezone.now()
                )
                log = LogTimeLine.objects.create(
                                policial=relatorio.policial,
                                texto=f"Foi rebaixado para o cargo de {proxima_patente}. Motivo: {relatorio.obs}",
                                datatime=timezone.now(),
                                requerimento='Rebaixamento'
                            )
                log.save()
                relatorio.status = 'Aprovado'
                relatorio.save()
            except User.DoesNotExist:
                messages.error(request, f"O policial com o username '{relatorio.policial}' não foi encontrado. Não é possível realizar o rebaixamento.")
        elif relatorio.requerimento == "Advertência":
            try:
                requerimento_user = User.objects.get(username=policial)
                LogRequerimento.objects.create(
                requerimento=relatorio,
                texto=f'O requerimento de {relatorio.requerimento} enviado por {relatorio.solicitante.patente} {relatorio.solicitante.username} foi aprovado por {request.user.username}.',
                datatime=timezone.now()
                )
                log = LogTimeLine.objects.create(
                                policial=relatorio.policial,
                                texto=f"{relatorio.obs}",
                                datatime=timezone.now(),
                                requerimento='Advertência'
                            )
                log.save()
                relatorio.status = 'Aprovado'
                relatorio.save()
            except User.DoesNotExist:
                messages.error(request, f"O policial com o username '{relatorio.policial}' não foi encontrado. Não é possível realizar a advertência.")
        elif relatorio.requerimento == "Banimento":     
            try:
                requerimento_user = User.objects.get(username=policial)
                LogRequerimento.objects.create(
                requerimento=relatorio,
                texto=f'O requerimento de {relatorio.requerimento} enviado por {relatorio.solicitante.patente} {relatorio.solicitante.username} foi aprovado por {request.user.username}.',
                datatime=timezone.now()
                )   
                log = LogTimeLine.objects.create(
                                policial=relatorio.policial,
                                texto=f"{relatorio.obs}",
                                datatime=timezone.now(),
                                requerimento='Banimento'
                            )
                log.save()
                requerimento_user.status = 'Banido'
                requerimento_user.save()
                relatorio.status = 'Aprovado'
                relatorio.save()
            except User.DoesNotExist:
                messages.error(request, f"O policial com o username '{relatorio.policial}' não foi encontrado. Não é possível realizar o banimento.")
        elif relatorio.requerimento == 'Demissão':
            try:
                requerimento_user = User.objects.get(username=policial)
                LogRequerimento.objects.create(
                requerimento=relatorio,
                texto=f'O requerimento de {relatorio.requerimento} enviado por {relatorio.solicitante.patente} {relatorio.solicitante.username} foi aprovado por {request.user.username}.',
                datatime=timezone.now()
                )
                log = LogTimeLine.objects.create(
                                policial=relatorio.policial,
                                texto=f"{relatorio.obs}",
                                datatime=timezone.now(),
                                requerimento='Demissão'
                            )
                log.save()
                requerimento_user.status = 'Demitido'
                requerimento_user.save()
                relatorio.status = 'Aprovado'
                relatorio.save()
            except User.DoesNotExist:
                messages.error(request, f"O policial com o username '{relatorio.policial}' não foi encontrado. Não é possível realizar a demissão.")
        elif relatorio.requerimento == "Contrato":
            requerimento_user = relatorio.policial.strip()

            if requerimento_user:
                User = get_user_model()
                try:
                    # Tenta encontrar um usuário com o username fornecido
                    aprovado_user = User.objects.get(username=policial)
                except User.DoesNotExist:
                    # Se o usuário não existir, cria um novo usuário
                    aprovado_user = User.objects.create_user(
                        username=requerimento_user,
                        password='fauiuaufauj20981428042',  # Defina uma senha padrão ou gere uma
                        patente=relatorio.cargo,
                    )

            LogRequerimento.objects.create(
            requerimento=relatorio,
            texto=f'O requerimento de {relatorio.requerimento} enviado por {relatorio.solicitante.patente} {relatorio.solicitante.username} foi aprovado por {request.user.username}.',
            datatime=timezone.now()
            )
            log = LogTimeLine.objects.create(
                            policial=relatorio.policial,
                            texto=f"{relatorio.obs}",
                            datatime=timezone.now(),
                            requerimento='Contrato'
                        )
            log.save()
            relatorio.status = 'Aprovado'
            relatorio.save()
        messages.success(request, f'Requerimento aprovado!')
        # Redirecionando para a página de relatórios gerais
        return HttpResponseRedirect(reverse('Requerimentos'))

@method_decorator(csrf_protect, name='dispatch')
class AdicionarLDPE(GroupRequiredMixin, View):
    template_name = 'Form.html'
    group_required = [u'STAFF']
    def post(self, request, user_id):
        user = get_object_or_404(PolicialUsuario, id=user_id)
        group = Group.objects.get(name='LDPE')
        user.groups.add(group)
        log = LogStaff.objects.create(
                    texto=f"{self.request.user} nomeou {user.username} como Líder do Departamento Educacional!",
                    datatime=timezone.now(),
                )
        log.save()
        messages.success(request, f'Você nomeou {user.username} como Líder do Departamento Educacional!')
        return redirect('LDPE')

@method_decorator(csrf_protect, name='dispatch')
class RemoverLDPE(GroupRequiredMixin, View):
    template_name = 'Form.html'
    group_required = [u'STAFF']
    def post(self, request, user_id):
        user = get_object_or_404(PolicialUsuario, id=user_id)
        group = Group.objects.get(name='LDPE')
        user.groups.remove(group)
        log = LogStaff.objects.create(
                    texto=f"{self.request.user} exonerou {user.username} como Líder do Departamento Educacional!",
                    datatime=timezone.now(),
                )
        log.save()
        messages.success(request, f'Você exonerou {user.username} como Líder do Departamento Educacional!')
        return redirect('LDPE')
    
@method_decorator(csrf_protect, name='dispatch')
class AdicionarLDRH(GroupRequiredMixin, View):
    template_name = 'Form.html'
    group_required = [u'STAFF']
    def post(self, request, user_id):
        user = get_object_or_404(PolicialUsuario, id=user_id)
        group = Group.objects.get(name='LDRH')
        user.groups.add(group)
        log = LogStaff.objects.create(
                    texto=f"{self.request.user} nomeou {user.username} como Líder do Departamento de Recursos Humanos!",
                    datatime=timezone.now(),
                )
        log.save()
        messages.success(request, f'Você nomeou {user.username} como Líder do Departamento de Recursos Humanos!')
        return redirect('LDRH')

@method_decorator(csrf_protect, name='dispatch')
class RemoverLDRH(GroupRequiredMixin, View):
    template_name = 'Form.html'
    group_required = [u'STAFF']
    def post(self, request, user_id):
        user = get_object_or_404(PolicialUsuario, id=user_id)
        group = Group.objects.get(name='LDRH')
        user.groups.remove(group)
        log = LogStaff.objects.create(
                    texto=f"{self.request.user} exonerou {user.username} como Líder do Departamento de Recursos Humanos!",
                    datatime=timezone.now(),
                )
        log.save()
        messages.success(request, f'Você exonerou {user.username} como Líder do Departamento de Recursos Humanos!')
        return redirect('LDRH')
    
class AdicionarEDC(GroupRequiredMixin, View):
    template_name = 'Form.html'
    group_required = [u'STAFF']
    def post(self, request, user_id):
        user = get_object_or_404(PolicialUsuario, id=user_id)
        group = Group.objects.get(name='EDC')
        user.groups.add(group)
        log = LogStaff.objects.create(
                    texto=f"{self.request.user} nomeou {user.username} como Editor-Chefe do Jornal!",
                    datatime=timezone.now(),
                )
        log.save()
        messages.success(request, f'Você nomeou {user.username} como Editor-Chefe do Jornal!')
        return redirect('EDC')

@method_decorator(csrf_protect, name='dispatch')
class RemoverEDC(GroupRequiredMixin, View):
    template_name = 'Form.html'
    group_required = [u'STAFF']
    def post(self, request, user_id):
        user = get_object_or_404(PolicialUsuario, id=user_id)
        group = Group.objects.get(name='EDC')
        user.groups.remove(group)
        log = LogStaff.objects.create(
                    texto=f"{self.request.user} exonerou {user.username} como Editor-Chefe do Jornal!",
                    datatime=timezone.now(),
                )
        log.save()
        messages.success(request, f'Você exonerou {user.username} como Editor-Chefe do Jornal!')
        return redirect('EDC')
    
@method_decorator(csrf_protect, name='dispatch')    
class AdicionarAnalista(GroupRequiredMixin, View):
    template_name = 'Form.html'
    group_required = [u'STAFF', u'LDRH']
    def post(self, request, user_id):
        user = get_object_or_404(PolicialUsuario, id=user_id)
        group = Group.objects.get(name='Analista')
        user.groups.add(group)
        log = LogStaff.objects.create(
                    texto=f"{self.request.user} nomeou {user.username} como Analista do Departamento de Recursos Humanos!",
                    datatime=timezone.now(),
                )
        log.save()
        messages.success(request, f'Você nomeou {user.username} como Analista do Departamento de Recursos Humanos!')
        return redirect('Analista')

@method_decorator(csrf_protect, name='dispatch')
class RemoverAnalista(GroupRequiredMixin, View):
    template_name = 'Form.html'
    group_required = [u'STAFF', u'LDRH']
    def post(self, request, user_id):
        user = get_object_or_404(PolicialUsuario, id=user_id)
        group = Group.objects.get(name='Analista')
        user.groups.remove(group)
        log = LogStaff.objects.create(
                    texto=f"{self.request.user} exonerou {user.username} como Analista do Departamento de Recursos Humanos",
                    datatime=timezone.now(),
                )
        log.save()
        messages.success(request, f'Você exonerou {user.username} como Analista do Departamento de Recursos Humanos!')
        return redirect('Analista')
    
class AnalistasView(GroupRequiredMixin, ListView):
    template_name = 'Analista.html'
    model = PolicialUsuario
    context_object_name = 'policiais'
    group_required = [u'STAFF', u'LDRH']
    
    def get_queryset(self):
        q = self.request.GET.get('q')
        grupo_membro = Group.objects.get(name='Analista')
        queryset = PolicialUsuario.objects.exclude(groups=grupo_membro).order_by('patente_order')

        if q:
            queryset = queryset.filter(username__icontains=q)

        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #Grupo de Jornalista 
        membro = 'Analista'
        #Lógica para testar os Militares se fazem parte dos grupos
        try:
            grupo_membro = Group.objects.get(name=membro)
            context['membros'] = PolicialUsuario.objects.filter(groups=grupo_membro).order_by('patente_order')
        except Group.DoesNotExist:
            context['membros'] = PolicialUsuario.objects.none()
        return context
    
class EDCView(GroupRequiredMixin, ListView):
    template_name = 'EDC.html'
    model = PolicialUsuario
    context_object_name = 'policiais'
    group_required = [u'STAFF']
    
    def get_queryset(self):
        q = self.request.GET.get('q')
        grupo_membro = Group.objects.get(name='EDC')
        queryset = PolicialUsuario.objects.exclude(groups=grupo_membro).order_by('patente_order')

        if q:
            queryset = queryset.filter(username__icontains=q)

        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #Grupo de Jornalista 
        membro = 'EDC'
        #Lógica para testar os Militares se fazem parte dos grupos
        try:
            grupo_membro = Group.objects.get(name=membro)
            context['membros'] = PolicialUsuario.objects.filter(groups=grupo_membro).order_by('patente_order')
        except Group.DoesNotExist:
            context['membros'] = PolicialUsuario.objects.none()
        return context
    
class LDRHView(GroupRequiredMixin, ListView):
    template_name = 'LDRH.html'
    model = PolicialUsuario
    context_object_name = 'policiais'
    group_required = [u'STAFF']
    
    def get_queryset(self):
        q = self.request.GET.get('q')
        grupo_membro = Group.objects.get(name='LDRH')
        queryset = PolicialUsuario.objects.exclude(groups=grupo_membro).order_by('patente_order')

        if q:
            queryset = queryset.filter(username__icontains=q)

        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #Grupo de Jornalista 
        membro = 'LDRH'
        #Lógica para testar os Militares se fazem parte dos grupos
        try:
            grupo_membro = Group.objects.get(name=membro)
            context['membros'] = PolicialUsuario.objects.filter(groups=grupo_membro).order_by('patente_order')
        except Group.DoesNotExist:
            context['membros'] = PolicialUsuario.objects.none()
        return context
    
class LDPEView(GroupRequiredMixin, ListView):
    template_name = 'LDPE.html'
    model = PolicialUsuario
    context_object_name = 'policiais'
    group_required = [u'STAFF']
    
    def get_queryset(self):
        q = self.request.GET.get('q')
        grupo_membro = Group.objects.get(name='LDPE')
        queryset = PolicialUsuario.objects.exclude(groups=grupo_membro).order_by('patente_order')

        if q:
            queryset = queryset.filter(username__icontains=q)

        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #Grupo de Jornalista 
        membro = 'LDPE'
        #Lógica para testar os Militares se fazem parte dos grupos
        try:
            grupo_membro = Group.objects.get(name=membro)
            context['membros'] = PolicialUsuario.objects.filter(groups=grupo_membro).order_by('patente_order')
        except Group.DoesNotExist:
            context['membros'] = PolicialUsuario.objects.none()
        return context
    
class STAFFView(GroupRequiredMixin, ListView):
    template_name = 'STAFF.html'
    model = PolicialUsuario
    context_object_name = 'policiais'
    group_required = [u'STAFF']
    
    def get_queryset(self):
        q = self.request.GET.get('q')
        grupo_membro = Group.objects.get(name='STAFF')
        queryset = PolicialUsuario.objects.exclude(groups=grupo_membro).order_by('patente_order')

        if q:
            queryset = queryset.filter(username__icontains=q)

        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #Grupo de Jornalista 
        membro = 'STAFF'
        #Lógica para testar os Militares se fazem parte dos grupos
        try:
            grupo_membro = Group.objects.get(name=membro)
            context['membros'] = PolicialUsuario.objects.filter(groups=grupo_membro).order_by('patente_order')
        except Group.DoesNotExist:
            context['membros'] = PolicialUsuario.objects.none()
        return context
    
@method_decorator(csrf_protect, name='dispatch')    
class AdicionarSTAFF(GroupRequiredMixin, View):
    template_name = 'Form.html'
    group_required = [u'STAFF']
    def post(self, request, user_id):
        user = get_object_or_404(PolicialUsuario, id=user_id)
        group = Group.objects.get(name='STAFF')
        user.groups.add(group)
        log = LogStaff.objects.create(
                    texto=f"{self.request.user} nomeou {user.username} como Saff!",
                    datatime=timezone.now(),
                )
        log.save()
        messages.success(request, f'Você nomeou {user.username} como Saff!')
        return redirect('STAFF')

@method_decorator(csrf_protect, name='dispatch')
class RemoverSTAFF(GroupRequiredMixin, View):
    template_name = 'Form.html'
    group_required = [u'STAFF']
    def post(self, request, user_id):
        user = get_object_or_404(PolicialUsuario, id=user_id)
        group = Group.objects.get(name='STAFF')
        user.groups.remove(group)
        log = LogStaff.objects.create(
                    texto=f"{self.request.user} exonerou {user.username} como Saff!",
                    datatime=timezone.now(),
                )
        log.save()
        messages.success(request, f'Você exonerou {user.username} como Saff!')
        return redirect('STAFF')
    
class RegistrarRequerimentoContrato(GroupRequiredMixin, CreateView):
    model = Requerimento
    template_name = 'Form.html'
    form_class = RequerimentoContratoForm
    group_required = [u'STAFF', u'LDRH', u'Analista']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = 'Registrar Requerimento'
        context["image"] = 'relatorio.png'
        context["descricao"] = 'Verifique todos os campos antes de registrar o requerimento!'
        return context
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.instance.solicitante = self.request.user
            form.instance.datatime = timezone.now()
            form.instance.requerimento = 'Contrato'
            new = form.save()

            try:
                log = LogRequerimento.objects.create(
                    requerimento=new,
                    texto=f"{new.solicitante} enviou um requerimento de {new.requerimento}",
                    datatime=timezone.now(),
                )
                log.save()
                messages.success(request, f'Requerimento registrado!')
            except Exception as e:
                print(f"Erro ao salvar o log: {e}")

            return HttpResponseRedirect(reverse('Requerimentos'))
        else:
            return self.form_invalid(form)
        
class LogTreinamentosView(GroupRequiredMixin, ListView):
    model = LogTreinamento
    template_name = 'Log.html'
    context_object_name = 'logs'
    group_required = [u'STAFF']
    def get_queryset(self):
        queryset = LogTreinamento.objects.all().order_by('-datatime')
        return queryset
    
class LogRequerimentoView(GroupRequiredMixin, ListView):
    model = LogRequerimento
    template_name = 'Log.html'
    context_object_name = 'logs'
    group_required = [u'STAFF']
    def get_queryset(self):
        queryset = LogRequerimento.objects.all().order_by('-datatime')
        return queryset
    
class LogJAView(GroupRequiredMixin, ListView):
    model = LogJA
    template_name = 'Log.html'
    context_object_name = 'logs'
    group_required = [u'STAFF']
    def get_queryset(self):
        queryset = LogJA.objects.all().order_by('-datatime')
        return queryset
    
class LogPostagemView(GroupRequiredMixin, ListView):
    model = LogPostagem
    template_name = 'Log.html'
    context_object_name = 'logs'
    group_required = [u'STAFF']
    def get_queryset(self):
        queryset = LogPostagem.objects.all().order_by('-datatime')
        return queryset
    
class LogStaffView(GroupRequiredMixin, ListView):
    model = LogStaff
    template_name = 'Log.html'
    context_object_name = 'logs'
    group_required = [u'STAFF']
    def get_queryset(self):
        queryset = LogStaff.objects.all().order_by('-datatime')
        return queryset
    
class LogDocumentosView(GroupRequiredMixin, ListView):
    model = LogDocumentos
    template_name = 'Log.html'
    context_object_name = 'logs'
    group_required = [u'STAFF']

    def get_queryset(self):
        queryset = LogDocumentos.objects.all().order_by('-datatime')
        return queryset

class LogTimeLineView(GroupRequiredMixin, ListView):
    model = LogTimeLine
    template_name = 'Log.html'
    context_object_name = 'logs'
    group_required = [u'STAFF']

    def get_queryset(self):
        queryset = LogTimeLine.objects.all().order_by('-datatime')
        return queryset
    
class PerfilPolicial(LoginRequiredMixin, DetailView):
    model = PolicialUsuario
    template_name = 'Perfil.html'
    context_object_name = 'perfil'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtenha o objeto MilitarUsuario atual
        policial = self.get_object()
        # Obtenha os emblemas comprados pelo militar
        emblemas_comprados = EmblemaCompra.objects.filter(solicitante=policial)
        # Adicione os emblemas ao contexto
        context['logs'] = LogTimeLine.objects.filter(policial=policial.username).order_by('-datatime')
        context['emblemas'] = emblemas_comprados
        return context
    
class ResetarSenha(GroupRequiredMixin, View):
    group_required = [u'STAFF', u'Analista', u'LDRH']
    @method_decorator(csrf_protect)
    def post(self, request, user_id):
        patentes_permitidas = [
            'Agente', 'Cabo', 'Sargento', 'Tenente', 'Capitão', 'Major', 'Coronel',
            'General', 'Comandante', 'Sócio', 'Inspetor', 'Inspetor-Chefe', 'Coordenador',
            'Supervisor', 'Administrador', 'Procurador', 'Ministro', 'Escrivão', 'Diretor',
            'Diretor-Fundador', 'Embaixador', 'Vice-Presidente', 'Presidente', 'Acionista',
            'Conselheiro'
        ]
        user = get_object_or_404(PolicialUsuario, id=user_id)
        if user.patente not in patentes_permitidas:
            # Se a patente não for permitida, exibe uma mensagem de erro
            messages.error(request, f'O policial {user.username} não pode ter sua senha resetada devido à patente.')
            return redirect('PoliciaisLista')
        
        log = LogRequerimento.objects.create(
                    texto=f"{request.user.username} resetou a senha do policial {user.username}",
                    datatime=timezone.now(),
                )
        log.save()
        user.set_password('123')
        user.save()
        messages.success(request, f'O policial {user.username} teve sua senha resetada: (123).')
        return redirect('PoliciaisLista')
    
class PoliciaisView(GroupRequiredMixin, ListView):
    template_name = 'PoliciaisLista.html'
    model = PolicialUsuario
    context_object_name = 'policiais'
    group_required = [u'STAFF', u'Analista', u'LDRH']
    
    def get_queryset(self):
        q = self.request.GET.get('q')
        patentes_permitidas = [
            'Agente', 'Cabo', 'Sargento', 'Tenente', 'Capitão', 'Major', 'Coronel',
            'General', 'Comandante', 'Sócio', 'Inspetor', 'Inspetor-Chefe', 'Coordenador',
            'Supervisor', 'Administrador', 'Procurador', 'Ministro', 'Escrivão', 'Diretor',
            'Diretor-Fundador', 'Embaixador', 'Vice-Presidente', 'Presidente', 'Acionista',
            'Conselheiro'
        ]
        queryset = PolicialUsuario.objects.filter(patente__in=patentes_permitidas).order_by('patente_order')

        if q:
            queryset = queryset.filter(username__icontains=q)

        return queryset
    
class PoliciaisStaffView(GroupRequiredMixin, ListView):
    template_name = 'PoliciaisListaStaff.html'
    model = PolicialUsuario
    context_object_name = 'policiais'
    group_required = [u'STAFF']
    
    def get_queryset(self):
        q = self.request.GET.get('q')

        queryset = PolicialUsuario.objects.all().order_by('patente_order')

        if q:
            queryset = queryset.filter(username__icontains=q)

        return queryset

class ResetarSenhaStaff(GroupRequiredMixin, View):
    group_required = [u'STAFF']
    @method_decorator(csrf_protect)
    def post(self, request, user_id):
        user = get_object_or_404(PolicialUsuario, id=user_id)
        log = LogRequerimento.objects.create(
                    texto=f"{request.user.username} resetou a senha do policial {user.username}",
                    datatime=timezone.now(),
                )
        log.save()
        user.set_password('123')
        user.save()
        messages.success(request, f'O policial {user.username} teve sua senha resetada: (123).')
        return redirect('PoliciaisLista')

class CriarDestaque(GroupRequiredMixin, CreateView):
    model = Destaques
    template_name = 'Form.html'
    form_class = DestaqueForm
    group_required = [u'STAFF']
    success_url = reverse_lazy('PainelPrincipal')


