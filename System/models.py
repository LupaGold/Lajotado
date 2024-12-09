from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django_ckeditor_5.fields import CKEditor5Field
from django.utils import timezone
import datetime
from django.utils.text import slugify
from ControleDeAcesso.models import CARGOS

REQUERIMENTO = (
          ('Promoção', 'Promoção'),
          ('Rebaixamento', 'Rebaixamento'),
          ('Advertência', 'Advertência'),
          ('Demissão', 'Demissão'),
          ('Banimento', 'Banimento'),
      )

STATUS = (
          ('Aprovado', 'Aprovado'),
          ('Em análise...', 'Em análise...'),
          ('Reprovado', 'Reprovado'),
      )

PROMOCAO = {
    'Agente': 'Cabo',
    'Cabo': 'Sargento',
    'Sargento': 'Tenente',
    'Tenente': 'Capitão',
    'Capitão': 'Major',
    'Major': 'Primeiro Sargento',
    'Primeiro Sargento': 'Subtenente',
    'Subtenente': 'Cadete',
    'Cadete': 'Aspirante-a-Oficial',
    'Aspirante-a-Oficial': 'Segundo Tenente',
    'Segundo Tenente': 'Primeiro Tenente',
    'Primeiro Tenente': 'Capitão',
    'Capitão': 'Major',
    'Major': 'Coronel',
    'Coronel': 'General',
    'General': 'Comandante',
    'Comandante': 'Sócio',
    'Sócio': 'Inspetor',
    'Inspetor': 'Inspetor-Chefe',
    'Inspetor-Chefe': 'Coordenador',
    'Coordenador': 'Supervisor',
    'Supervisor': 'Administrador',
    'Administrador': 'Procurador',
    'Procurador': 'Ministro',
    'Ministro': 'Escrivão',
    'Escrivão': 'Diretor',
    'Diretor': 'Diretor-Fundador',
    'Diretor-Fundador': 'Embaixador',
    'Embaixador': 'Vice-Presidente',
    'Vice-Presidente': 'Presidente',
    'Presidente': 'Acionista',
    'Acionista': 'Conselheiro',
    'Conselheiro': 'Suplente',
    'Suplente': 'Co-Fundador',
    'Co-Fundador': 'Sub-Fundador',
    'Sub-Fundador': 'Fundador',
    'Fundador': 'Supremo', 
}

#Model do post do fórum
class Post(models.Model):
      #Data do post
      data = models.DateTimeField(blank=False, null=True, default=timezone.now)
      #Autor do post
      autor = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,blank=True, null=True)
      #Texto do post
      texto = models.TextField(blank=False, null=True, verbose_name='Texto', max_length=300)
      
      def __str__(self):
        return str(self.autor)

#Model dos comentarios de post do forum
class Comentario(models.Model):
    #Data do comentario
    data = models.DateTimeField(blank=False, null=True, default=timezone.now)
    #Post vinculado
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comentarios')
    #Autor do comentário
    autor = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,blank=True, null=True, related_name='comentarioautor')
    #Texto do post
    texto = models.TextField()

#Aval para afastamento não remunerado
class JA(models.Model):
      #Data e tempo de criação
      datatime = models.DateTimeField(default=timezone.now)
      #Militar que enviou o JA
      solicitante = models.ForeignKey(get_user_model(), on_delete=models.PROTECT,blank=True, null=True)
      #Motivo do Aval
      motivo = models.TextField(blank=False, null=True, verbose_name='Motivo', max_length=150)
      #Data de início e de fim
      data = models.DateField(blank=False, null=True, default=datetime.date.today)
      data2 = models.DateField(blank=False, null=True, default=datetime.date.today)
      #Status do JA
      status = models.CharField(choices=STATUS, blank=False, null=True, max_length=50, default='Em análise...')
      
      def __str__(self):
        return f'Aval solicitado por {self.solicitante.patente} {self.solicitante.username}, com início em {self.data} e termino em {self.data2}; Atual status: {self.status}.'
      
class LogJA(models.Model):
      #Aval relacionado a log
      aval = models.ForeignKey(JA, verbose_name=("aval"), on_delete=models.PROTECT)
      #Texto da log
      texto = models.TextField(blank=False, null=True, verbose_name='Texto Aval', max_length=150)
      #Data e tempo de criação da log
      datatime = models.DateTimeField(default=timezone.now)

      def __str__(self):
        return f'{{{self.texto})}}'

#Class de emblemas da loja
class EmblemasModel(models.Model):
    #Militar responsável pela alteração na honraria
    solicitante = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,blank=True, null=True, related_name='solicitanteemblemas')
    #Título da pagina
    titulo = models.TextField(blank=False, null=True, max_length=30)
    #Valor do emblema
    moedas = models.IntegerField(default=0)
    #Data do envio
    datatime = models.DateTimeField(default=timezone.now)
    #Icone da honraria
    icone = models.ImageField(upload_to='imagens/')

    def __str__(self):
        return self.titulo

class EmblemaCompra(models.Model):
    #Militar responsável pela alteração na honraria
    solicitante = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,blank=True, null=True, related_name='comprador')
    #Emblema relacionado
    emblema = models.ForeignKey(EmblemasModel, on_delete=models.CASCADE,blank=True, null=True)

    def __str__(self):
        return f'{self.emblema} comprado por {self.solicitante}'
    
class PostagemJornal(models.Model):
    #Jornalista responsável pela postagem
    solicitante = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,blank=True, null=True, related_name='solicitantepostagem')
    #Título da postagem
    titulo = models.TextField(blank=False, null=True, max_length=90)
    #Descrição
    descricao = models.TextField(blank=False, null=True, max_length=170)
    #Treinamento escrito no Editor de texto
    texto = CKEditor5Field('Postagem', config_name='extends', default=' ')
    #Data e tempo de atualização do treinamento
    datatime = models.DateTimeField(default=timezone.now)
    #Imagem do banner da postagem
    imagem = models.ImageField(upload_to='imagens/')
    # Slug para URL amigável
    slug = models.SlugField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Postagem ({self.titulo} postado por {self.solicitante.username} em {self.datatime})'
    
class LogPostagem(models.Model):
      #Treinamento relacionado a log
      treinamento = models.ForeignKey(PostagemJornal, verbose_name=("postagem"), on_delete=models.PROTECT, null=True)
      #Texto da log
      texto = models.TextField(blank=False, null=True, verbose_name='Texto postagem', max_length=150)
      #Data e tempo de criação da log
      datatime = models.DateTimeField(default=timezone.now)

      def __str__(self):
        return f'{{{self.texto})}}'
      
class Treinamentos(models.Model):
    #Usuário que registrou o treinamento
    solicitante = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,blank=True, null=True, related_name='solicitantetreinamentos')
    #Título do treinamento
    titulo = models.TextField(blank=False, null=True, max_length=100)
    #Treinamento escrito no Editor de texto
    treinamento = CKEditor5Field('Treinamentos', config_name='extends', default=' ')
    #Data e tempo de atualização do treinamento
    datatime = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.titulo
    
class LogTreinamento(models.Model):
      #Treinamento relacionado a log
      treinamento = models.ForeignKey(Treinamentos, verbose_name=("treinamento"), on_delete=models.PROTECT, null=True)
      #Texto da log
      texto = models.TextField(blank=False, null=True, verbose_name='Texto relatorio', max_length=150)
      #Data e tempo de criação da log
      datatime = models.DateTimeField(default=timezone.now)

      def __str__(self):
        return f'{{{self.texto})}}'
      
class RelatorioTreinamento(models.Model):
    #Data e tempo de postagem
    datatime = models.DateTimeField(default=timezone.now)
    #Usuário que registrou o treinamento
    solicitante = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,blank=True, null=True, related_name='solicitanterelatorio')
    #Treinamento
    treinamento = models.ForeignKey(Treinamentos, blank=False, null=False, on_delete=models.CASCADE)
    #Aprovado
    aprovado = models.TextField(blank=True, null=True, max_length=70)
    #Reprovado
    reprovado = models.TextField(blank=True, null=True, max_length=70)
    #Obs
    obs = models.TextField(blank=False, null=True, verbose_name='Observações', max_length=150)
    #Status
    status = models.CharField(choices=STATUS, blank=False, null=True, max_length=50, default='Em análise...')

    def __str__(self):
        return f'{{{self.treinamento.titulo}, {self.datatime} por {self.solicitante.username}.}}'

class Documentos(models.Model):
    #Usuário que registrou o treinamento
    solicitante = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,blank=True, null=True, related_name='solicitantedocumentos')
    #Título do treinamento
    titulo = models.TextField(blank=False, null=True, max_length=30)
    #Treinamento escrito no Editor de texto
    documentos = CKEditor5Field('Documentos', config_name='extends', default=' ')
    #Data e tempo de atualização do treinamento
    datatime = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.titulo
    
class LogDocumentos(models.Model):
      #Treinamento relacionado a log
      treinamento = models.ForeignKey(Documentos, verbose_name=("documentis"), on_delete=models.PROTECT, null=True)
      #Texto da log
      texto = models.TextField(blank=False, null=True, verbose_name='Texto relatorio', max_length=150)
      #Data e tempo de criação da log
      datatime = models.DateTimeField(default=timezone.now)

      def __str__(self):
        return f'{{{self.texto})}}'
      
class Requerimento(models.Model):
    #Data e tempo de postagem
    datatime = models.DateTimeField(default=timezone.now)
    #Usuário que registrou o treinamento
    solicitante = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,blank=True, null=True, related_name='solicitanterequerimento')
    #Aprovado
    policial = models.TextField(blank=True, null=True, max_length=70,verbose_name='Policial')

    cargo = models.CharField(choices=CARGOS, blank=True, null=True, max_length=50, default='Agente')
    #Obs
    obs = models.TextField(blank=False, null=True, verbose_name='Observações', max_length=150)
    #Requerimento
    requerimento = models.CharField(choices=REQUERIMENTO, blank=False, null=True, max_length=50, verbose_name='Tipo')
    #Status
    status = models.CharField(choices=STATUS, blank=False, null=True, max_length=50, default='Em análise...')

    def __str__(self):
        return f'{{{self.requerimento} do policial {self.policial}, {self.datatime} por {self.solicitante.username}. Motivo: {self.obs}}}'
    
class LogTimeLine(models.Model):
      policial = models.TextField(blank=False, null=True, verbose_name='Policial', max_length=150)
      #Texto da log
      texto = models.TextField(blank=False, null=True, verbose_name='Texto', max_length=150)
      #Data e tempo de criação da log
      datatime = models.DateTimeField(default=timezone.now)

      requerimento = models.CharField(choices=REQUERIMENTO, blank=False, null=True, max_length=50, verbose_name='Tipo')

      def __str__(self):
        return f'{{{self.texto})}}'

class LogRequerimento(models.Model):
      #Treinamento relacionado a log
      requerimento = models.ForeignKey(Requerimento, verbose_name=("requerimento"), on_delete=models.PROTECT, null=True)
      #Texto da log
      texto = models.TextField(blank=False, null=True, verbose_name='Texto requerimento', max_length=150)
      #Data e tempo de criação da log
      datatime = models.DateTimeField(default=timezone.now)

      def __str__(self):
        return f'{{{self.texto})}}'
      
class LogStaff(models.Model):
      #Texto da log
      texto = models.TextField(blank=False, null=True, verbose_name='Texto relatorio', max_length=150)
      #Data e tempo de criação da log
      datatime = models.DateTimeField(default=timezone.now)

      def __str__(self):
        return f'{{{self.texto})}}'
      
class Destaques(models.Model):

    destaque1 = models.TextField(blank=False, null=True, verbose_name='Destaque', max_length=150)

    destaque2 = models.TextField(blank=False, null=True, verbose_name='Destaque', max_length=150)

    def __str__(self):
        return f'{{{self.destaque1} {self.destaque2})}}'
    
class LogDPO(models.Model):
      #Texto da log
      texto = models.TextField(blank=False, null=True, verbose_name='Texto relatorio', max_length=150)
      #Data e tempo de criação da log
      datatime = models.DateTimeField(default=timezone.now)

      def __str__(self):
        return f'{{{self.texto})}}'
      
class DPORelatório(models.Model):
    #Data e tempo de atualização do treinamento
    datatime = models.DateTimeField(default=timezone.now)
    #Usuário que registrou o treinamento
    solicitante = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,blank=True, null=True, related_name='solicitantedpo')
    #Contador
    militares = models.IntegerField(default=0, editable=True)
    #Contador
    fundação = models.IntegerField(default=0, editable=True)
    #Contador
    motivo = models.TextField(blank=False, null=True, max_length=170)
    #Imagem do banner da postagem
    imagem = models.ImageField(upload_to='imagens/')

      
class DPOBanimento(models.Model):
    #Data e tempo de atualização do treinamento
    datatime = models.DateTimeField(default=timezone.now)
    #Usuário que registrou o treinamento
    solicitante = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,blank=True, null=True, related_name='solicitantedpobanimento')
    #Contador
    resp = models.TextField(blank=False, null=True, max_length=170, verbose_name='Responsável')
    #Contador
    banido = models.TextField(blank=False, null=True, max_length=170)
    #Contador
    fundação = models.IntegerField(default=0, editable=True)
    #Contador
    motivo = models.TextField(blank=False, null=True, max_length=170)
    #Imagem do banner da postagem
    imagem = models.ImageField(upload_to='imagens/')

class Lota(models.Model):
    #Data e tempo de atualização do treinamento
    datatime = models.DateTimeField(default=timezone.now)
    #Usuário que registrou o treinamento
    solicitante = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,blank=True, null=True, related_name='solicitantelota')
    #Contador
    lotador = models.TextField(blank=False, null=True, max_length=170)
    #Contador
    recruta = models.TextField(blank=False, null=True, max_length=170)
    #Imagem do banner da postagem
    imagem = models.ImageField(upload_to='imagens/')

class LogLota(models.Model):
      #Texto da log
      texto = models.TextField(blank=False, null=True, verbose_name='Texto relatorio', max_length=150)
      #Data e tempo de criação da log
      datatime = models.DateTimeField(default=timezone.now)

      def __str__(self):
        return f'{{{self.texto})}}'