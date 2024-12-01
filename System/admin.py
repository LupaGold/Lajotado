from django.contrib import admin
from .models import (EmblemasModel, PostagemJornal, LogPostagem, JA, LogJA, 
                     Treinamentos, LogTreinamento, RelatorioTreinamento, 
                     Documentos, LogDocumentos, LogRequerimento, LogTimeLine,
                     LogStaff, Requerimento, Destaques)
# Register your models here.
admin.site.register(EmblemasModel)
admin.site.register(PostagemJornal)
admin.site.register(LogPostagem)
admin.site.register(JA)
admin.site.register(LogJA)
admin.site.register(Treinamentos)
admin.site.register(LogTreinamento)
admin.site.register(RelatorioTreinamento)
admin.site.register(Documentos)
admin.site.register(LogDocumentos)
admin.site.register(LogRequerimento)
admin.site.register(LogTimeLine)
admin.site.register(LogStaff)
admin.site.register(Requerimento)
admin.site.register(Destaques)