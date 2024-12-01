import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import BaseUserManager
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _
from django.utils.text import slugify

STATUS = (
          ('Ativo','Ativo'),
          ('Demitido','Demitido'),
          ('Banido','Banido'),
)

CARGOS = (
          ('', 'Selecione a Patente'),
          ('Agente','Agente'),
          ('Cabo','Cabo'),
          ('Sargento','Sargento'),
          ('Tenente','Tenente'),
          ('Capitão','Capitão'),
          ('Major','Major'),
          ('Coronel','Coronel'),
          ('General','General'),
          ('Comandante','Comandante'),
          ('Sócio','Sócio'),
          ('Inspetor','Inspetor'),
          ('Inspetor-Chefe','Inspetor-Chefe'),
          ('Coordenador','Coordenador'),
          ('Supervisor','Supervisor'),
          ('Administrador','Administrador'),
          ('Procurador','Procurador'),
          ('Ministro','Ministro'),
          ('Escrivão','Escrivão'),
          ('Diretor','Diretor'),
          ('Diretor-Fundador','Diretor-Fundador'),
          ('Embaixador','Embaixador'),
          ('Vice-Presidente','Vice-Presidente'),
          ('Presidente','Presidente'),
          ('Acionista','Acionista'),
          ('Conselheiro','Conselheiro'),
          ('Suplente','Suplente'),
          ('Co-Fundador','Co-Fundador'),
          ('Sub-Fundador','Sub-Fundador'),
          ('Fundador','Fundador'),
          ('Supremo','Supremo'),
      )

#Manager do MilitarUsuario
class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('O nome de usuário é obrigatório')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser deve ter is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser deve ter is_superuser=True.')

        return self.create_user(username, password, **extra_fields)

#Model Policial
class PolicialUsuario(AbstractUser):
    #Alteração no validador para incluir caracteres inválidos
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        validators=[RegexValidator(
            regex=r'^[a-zA-Z0-9@_:.,\-!=]+$',
            message=_('Enter a valid username. This value may contain only letters (uppercase and lowercase), numbers, @, :, -, and _ characters.'),
            code='invalid_username',
        )],
        help_text=_('150 characters or fewer. Letters (uppercase and lowercase), digits, @, :, -, and _ only.'),
    )
    #Patente do Militar
    patente = models.CharField(choices=CARGOS, blank=False, null=False, max_length=50, default='Agente')
    #Moedas na carteira
    moedas = models.IntegerField(default=0, editable=True)
    #Log de IP
    ultimo_acesso = models.DateTimeField(null=True, blank=True)
    #Definindo o manage
    objects = CustomUserManager()
    #Ordem de patentes
    patente_order = models.IntegerField(default=0, editable=False)
    # Slug para URL amigável
    slug = models.SlugField(unique=True, blank=True, null=True)
    
    status = models.CharField(choices=STATUS, blank=False, null=False, max_length=50, default='Ativo')
    def save(self, *args, **kwargs):
        patente_order_map = {
            'Supremo': 1,
            'Fundador': 2,
            'Sub-Fundador': 3,
            'Co-Fundador': 4,
            'Suplente': 5,
            'Conselheiro': 6,
            'Acionista': 7,
            'Presidente': 8,
            'Vice-Presidente': 9,
            'Embaixador': 10,
            'Diretor-Fundador': 11,
            'Diretor': 12,
            'Escrivão': 13,
            'Ministro': 14,
            'Procurador': 15, 
            'Administrador': 16,
            'Supervisor': 17, 
            'Coordenador': 18, 
            'Inspetor-Chefe': 19,
            'Inspetor': 20,
            'Sócio': 21,
            'Comandante': 22,
            'General': 23,
            'Coronel': 24,
            'Major': 25,
            'Capitão': 26,
            'Tenente': 27,
            'Sargento': 28,
            'Cabo': 29,
            'Agente': 30,
        }
        # Definir a ordem da patente com base no mapa
        self.patente_order = patente_order_map.get(self.patente, 99)

        # Gerar slug a partir do username se o slug estiver vazio
        if not self.slug:
            base_slug = slugify(self.username)
            slug = base_slug
            n = 1
            while PolicialUsuario.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{n}"
                n += 1
            self.slug = slug

        # Chamar o método save() da superclasse
        super().save(*args, **kwargs)

    def __str__(self):
            return f"{self.username}, {self.patente}"