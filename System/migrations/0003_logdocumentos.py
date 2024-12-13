# Generated by Django 5.1.3 on 2024-11-29 18:42

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('System', '0002_documentos'),
    ]

    operations = [
        migrations.CreateModel(
            name='LogDocumentos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto', models.TextField(max_length=150, null=True, verbose_name='Texto relatorio')),
                ('datatime', models.DateTimeField(default=django.utils.timezone.now)),
                ('treinamento', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='System.documentos', verbose_name='documentis')),
            ],
        ),
    ]
