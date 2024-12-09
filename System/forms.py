from django import forms
from .models import (Comentario, Post, JA, PostagemJornal, Treinamentos, 
                     RelatorioTreinamento, Documentos, Requerimento, Destaques,
                     DPOBanimento, DPORelatório, Lota)
from django_ckeditor_5.widgets import CKEditor5Widget

#Form do comentario
class ComentarioForm(forms.ModelForm):
    texto = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 1, 'placeholder': 'Digite aqui...'}), label='', max_length=150)

    class Meta:
        model = Comentario
        fields = ['texto']

#Form do post
class PostForm(forms.ModelForm):
    texto = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Digite aqui...'}), label='', max_length=150)

    class Meta:
        model = Post
        fields = ['texto']

#Formulário de envio de JA's
class JAForm(forms.ModelForm):
    #Campos
    motivo = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Digite o motivo do afastamento aqui.'}), label='Motivo:', max_length=150)
    data = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}), label='Data de Ida:')
    data2 = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}), label='Data de Volta:')

    #Meta dos campos
    class Meta:
        model = JA
        fields = ['motivo', 'data', 'data2']

class PostagemForm(forms.ModelForm):
    class Meta:
        model = PostagemJornal
        fields = ['titulo','descricao', 'texto', 'imagem',]
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control'}),
            'texto': CKEditor5Widget(),
        }

class TreinamentosForm(forms.ModelForm):
    class Meta:
        model = Treinamentos
        fields = ['titulo','treinamento',]
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'treinamento': CKEditor5Widget(),
        }

class RelatorioForm(forms.ModelForm):
    class Meta:
        model = RelatorioTreinamento
        fields = ['treinamento', 'aprovado', 'reprovado','obs']
        widgets = {
            'treinamento': forms.Select(attrs={'class': 'form-control'}),
            'aprovado': forms.TextInput(attrs={'class': 'form-control'}),
            'reprovado': forms.TextInput(attrs={'class': 'form-control'}),
            'obs': forms.Textarea(attrs={'class': 'form-control'}),
        }

class DocumentosForm(forms.ModelForm):
    class Meta:
        model = Documentos
        fields = ['titulo','documentos',]
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'documentos': CKEditor5Widget(),
        }

class RequerimentoForm(forms.ModelForm):
    class Meta:
        model = Requerimento
        fields = ['requerimento','policial','obs',]
        widgets = {
            'requerimento': forms.Select(attrs={'class': 'form-control'}),
            'policial': forms.TextInput(attrs={'class': 'form-control'}),
            'obs': forms.TextInput(attrs={'class': 'form-control'}),
        }

class RequerimentoContratoForm(forms.ModelForm):
    class Meta:
        model = Requerimento
        fields = ['policial','cargo','obs']
        widgets = {
            'policial': forms.TextInput(attrs={'class': 'form-control'}),
            'cargo': forms.Select(attrs={'class': 'form-control'}),
            'obs': forms.TextInput(attrs={'class': 'form-control'}),
        }

class DestaqueForm(forms.ModelForm):
    class Meta:
        model = Destaques
        fields = ['destaque1','destaque2']
        widgets = {
            'destaque1': forms.TextInput(attrs={'class': 'form-control'}),
            'destaque2': forms.TextInput(attrs={'class': 'form-control'}),
        }

class DPORelatórioForm(forms.ModelForm):
    class Meta:
        model = DPORelatório
        fields = ['militares','fundação', 'motivo', 'imagem',]
        widgets = {
            'militares': forms.NumberInput(attrs={'class': 'form-control'}),
            'fundação': forms.NumberInput(attrs={'class': 'form-control'}),
            'motivo': forms.TextInput(attrs={'class': 'form-control'}),
        }

class DPOBanimentoForm(forms.ModelForm):
    class Meta:
        model = DPOBanimento
        fields = ['resp','banido', 'fundação', 'motivo','imagem',]
        widgets = {
            'resp': forms.TextInput(attrs={'class': 'form-control','label':'Responsável'}),
            'banido': forms.TextInput(attrs={'class': 'form-control'}),
            'fundação': forms.TextInput(attrs={'class': 'form-control'}),
            'motivo': forms.TextInput(attrs={'class': 'form-control'}),
        }

class LotaForm(forms.ModelForm):
    class Meta:
        model = Lota
        fields = ['lotador','recruta','imagem']
        widgets = {
            'lotador': forms.TextInput(attrs={'class': 'form-control'}),
            'recruta': forms.TextInput(attrs={'class': 'form-control'}),
        }