from django.urls import path, include
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.shortcuts import redirect
from ControleDeAcesso.views import AlterarSenhaView
from .views import (
    PainelPrincipal, MeusAvais, RegistrarAval, AprovarAvalView, 
    RejeitarAvalView, AvaisGeral, LojaEmblemasView, ComprarEmblemaView,
    JornalPrincipal,Postagens, RegistrarPostagem, EditarPostagem,
    AdicionarJornalista, RemoverJornalista,Jornalistas, TreinamentosView,
    RegistrarTreinamento, RelatoriosTreinamentos, RegistrarRelatorioTreinamento,
    RelatorioGeral,EditarTreinamento, AprovarRelatorio, ReprovarRelatorio,
    AdicionarGuia, AdicionarMinistroDpE, RemoverGuia, RemoverMinistroDpE,
    GuiasDpEView, MinistroDpEView, DocumentosView, EditarDocumentos, RegistrarDocumento,
    Requerimentos, RegistrarRequerimento, AprovarRequerimento, ReprovarRequerimento,
    AdicionarAnalista, RemoverAnalista, AdicionarEDC, RemoverEDC, AdicionarLDPE, RemoverLDPE,
    AdicionarLDRH, RemoverLDRH, LDPEView, LDRHView, AnalistasView, EDCView, AdicionarSTAFF, 
    RemoverSTAFF, STAFFView, RegistrarRequerimentoContrato, LogTreinamentosView, LogRequerimentoView,
    LogDocumentosView, LogTimeLineView, LogPostagemView, LogStaffView,LogJAView, PerfilPolicial,
    ResetarSenha, PoliciaisView, ResetarSenhaStaff, PoliciaisStaffView, CriarDestaque
    )

def custom_logout(request):
    logout(request)
    return redirect(reverse_lazy('LoginPainel'))

urlpatterns = [
    path('principal/', PainelPrincipal.as_view(), name='PainelPrincipal'),
    path('minhas-licenças/', MeusAvais.as_view(), name='MeusAvais'),
    path('geral-licenças/', AvaisGeral.as_view(), name='GeralAvais'),
    path('perfil/<slug:slug>/', PerfilPolicial.as_view(), name='PerfilPolicial'),
    path('registrar-licença/', RegistrarAval.as_view(), name='RegistrarAval'),
    path('geral-licenças/aprovar/<int:ja_id>/', AprovarAvalView.as_view(), name='AprovarAval'),
    path('geral-licenças/rejeitar/<int:ja_id>/', RejeitarAvalView.as_view(), name='RejeitarAval'),
    path('loja/', LojaEmblemasView.as_view(), name='Loja'),
    path('loja/comprar/<int:emblema_id>/', ComprarEmblemaView.as_view(), name='ComprarEmblema'),
    path('alterar-senha/', AlterarSenhaView.as_view(), name='AlterarSenha'),
    path('jornal/', JornalPrincipal.as_view(), name='Jornal'),
    path('jornal/postagens/<slug:slug>/', Postagens.as_view(), name='PostagensJornal'),
    path('jornal/publicar-materia/', RegistrarPostagem.as_view(), name='PublicarMateria'),
    path('jornal/editar-materia/<slug:slug>/', EditarPostagem.as_view(), name='EditarMateria'),
    path('jornalistas/', Jornalistas.as_view(), name='Jornalistas'),
    path('jornalistas/adicionar/<int:user_id>/', AdicionarJornalista.as_view(), name='AdicionarJornalista'),
    path('jornalistas/remover/<int:user_id>/', RemoverJornalista.as_view(), name='RemoverJornalista'),
    path('dpe/treinamentos/', TreinamentosView.as_view(), name='Treinamentos'),
    path('dpe/registar-treinamentos/', RegistrarTreinamento.as_view(), name='RegistrarTreinamentos'),
    path('dpe/meus-relatorios/', RelatoriosTreinamentos.as_view(), name='RelatoriosTreinamentos'),
    path('dpe/registrar-relatorio/', RegistrarRelatorioTreinamento.as_view(), name='RegistrarRelatorioTreinamento'),
    path('dpe/relatorios-geral/', RelatorioGeral.as_view(), name='RelatoriosGeral'),
    path('dpe/editar-treinamento/<int:pk>/', EditarTreinamento.as_view(), name='EditarTreinamento'),
    path('dpe/aprovar-treinamento/<int:relatorio_id>/', AprovarRelatorio.as_view(), name='AprovarRelatorio'),
    path('dpe/reprovar-treinamento/<int:relatorio_id>/', ReprovarRelatorio.as_view(), name='ReprovarRelatorio'),
    path('dpe/guias/', GuiasDpEView.as_view(), name='GuiasDpE'),
    path('dpe/ministros/', MinistroDpEView.as_view(), name='MinistrosDpE'),
    path('dpe/adicionar-guia/<int:user_id>/', AdicionarGuia.as_view(), name='AdicionarGuia'),
    path('dpe/remover-guia/<int:user_id>/', RemoverGuia.as_view(), name='RemoverGuia'),
    path('dpe/adicionar-ministro/<int:user_id>/', AdicionarMinistroDpE.as_view(), name='AdicionarMinistroDpE'),
    path('dpe/removerministro/<int:user_id>/', RemoverMinistroDpE.as_view(), name='RemoverMinistroDpE'),
    path('documentos/', DocumentosView.as_view(), name='Documentos'),
    path('documentos/registar-documento/', RegistrarDocumento.as_view(), name='RegistrarDocumento'),
    path('documentos/editar-documento/<int:pk>/', EditarDocumentos.as_view(), name='EditarDocumentos'),
    path('drh/requerimentos/', Requerimentos.as_view(), name='Requerimentos'),
    path('drh/registrar-requerimentos-contrato/', RegistrarRequerimentoContrato.as_view(), name='RegistrarRequerimentoContrato'),
    path('drh/registrar-requerimentos/', RegistrarRequerimento.as_view(), name='RegistrarRequerimento'),
    path('drh/aprovar-requerimento/<int:relatorio_id>/', AprovarRequerimento.as_view(), name='AprovarRequerimento'),
    path('drh/reprovar-requerimento/<int:relatorio_id>/', ReprovarRequerimento.as_view(), name='ReprovarRequerimento'),
    path('drh/adicionar/<int:user_id>/', AdicionarAnalista.as_view(), name='AdicionarAnalista'),
    path('drh/remover/<int:user_id>/', RemoverAnalista.as_view(), name='RemoverAnalista'),
    path('drh/analistas/', AnalistasView.as_view(), name='Analista'),
    path('drh/policiais-lista/', PoliciaisView.as_view(), name='PoliciaisLista'),
    path('drh/policiais-lista/alterar-senha/<int:user_id>/', ResetarSenha.as_view(), name='ResetarSenha'),
    path('staff/dpe/', LDPEView.as_view(), name='LDPE'),
    path('staff/drh/', LDRHView.as_view(), name='LDRH'),
    path('staff/jornal/', EDCView.as_view(), name='EDC'),
    path('staff/membros/', STAFFView.as_view(), name='STAFF'),
    path('staff/log-ja/', LogJAView.as_view(), name='LOGJA'),
    path('staff/log-documentos/', LogDocumentosView.as_view(), name='LOGDOCUMENTOS'),
    path('staff/log-postagens/', LogPostagemView.as_view(), name='LOGPOSTAGENS'),
    path('staff/log-requerimentos/', LogRequerimentoView.as_view(), name='LOGREQUERIMENTOS'),
    path('staff/log-treinamentos/', LogTreinamentosView.as_view(), name='LOGTREINAMENTOS'),
    path('staff/log-staff/', LogStaffView.as_view(), name='LOGSTAFF'),
    path('staff/criar-destaque/', CriarDestaque.as_view(), name='CriarDestaque'),
    path('staff/log-timeline/', LogTimeLineView.as_view(), name='LOGTIMELINE'),
    path('staff/policiais-lista/', PoliciaisStaffView.as_view(), name='PoliciaisListaStaff'),
    path('staff/policiais-lista/alterar-senha/<int:user_id>/', ResetarSenhaStaff.as_view(), name='ResetarSenhaStaff'),
    path('staff/dpe/adicionar/<int:user_id>/', AdicionarLDPE.as_view(), name='AdicionarLDPE'),
    path('staff/dpe/remover/<int:user_id>/', RemoverLDPE.as_view(), name='RemoverLDPE'),
    path('staff/drh/adicionar/<int:user_id>/', AdicionarLDRH.as_view(), name='AdicionarLDRH'),
    path('staff/drh/remover/<int:user_id>/', RemoverLDRH.as_view(), name='RemoverLDRH'),
    path('staff/jornal/adicionar/<int:user_id>/', AdicionarEDC.as_view(), name='AdicionarEDC'),
    path('staff/jornal/remover/<int:user_id>/', RemoverEDC.as_view(), name='RemoverEDC'),
    path('staff/membros/adicionar/<int:user_id>/', AdicionarSTAFF.as_view(), name='AdicionarSTAFF'),
    path('staff/membros/remover/<int:user_id>/', RemoverSTAFF.as_view(), name='RemoverSTAFF'),
]