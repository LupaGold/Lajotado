# Generated by Django 5.1.3 on 2024-12-01 03:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('System', '0009_logstaff'),
    ]

    operations = [
        migrations.AddField(
            model_name='requerimento',
            name='cargo',
            field=models.CharField(blank=True, choices=[('', 'Selecione a Patente'), ('Agente', 'Agente'), ('Cabo', 'Cabo'), ('Sargento', 'Sargento'), ('Tenente', 'Tenente'), ('Capitão', 'Capitão'), ('Major', 'Major'), ('Coronel', 'Coronel'), ('General', 'General'), ('Comandante', 'Comandante'), ('Sócio', 'Sócio'), ('Inspetor', 'Inspetor'), ('Inspetor-Chefe', 'Inspetor-Chefe'), ('Coordenador', 'Coordenador'), ('Supervisor', 'Supervisor'), ('Administrador', 'Administrador'), ('Procurador', 'Procurador'), ('Ministro', 'Ministro'), ('Escrivão', 'Escrivão'), ('Diretor', 'Diretor'), ('Diretor-Fundador', 'Diretor-Fundador'), ('Embaixador', 'Embaixador'), ('Vice-Presidente', 'Vice-Presidente'), ('Presidente', 'Presidente'), ('Acionista', 'Acionista'), ('Conselheiro', 'Conselheiro'), ('Suplente', 'Suplente'), ('Co-Fundador', 'Co-Fundador'), ('Sub-Fundador', 'Sub-Fundador'), ('Fundador', 'Fundador'), ('Supremo', 'Supremo')], default='Agente', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='logtimeline',
            name='requerimento',
            field=models.CharField(choices=[('Promoção', 'Promoção'), ('Rebaixamento', 'Rebaixamento'), ('Advertência', 'Advertência'), ('Demissão', 'Demissão'), ('Banimento', 'Banimento')], max_length=50, null=True, verbose_name='Tipo'),
        ),
        migrations.AlterField(
            model_name='requerimento',
            name='requerimento',
            field=models.CharField(choices=[('Promoção', 'Promoção'), ('Rebaixamento', 'Rebaixamento'), ('Advertência', 'Advertência'), ('Demissão', 'Demissão'), ('Banimento', 'Banimento')], max_length=50, null=True, verbose_name='Tipo'),
        ),
    ]
