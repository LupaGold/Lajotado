# Generated by Django 5.1.3 on 2024-12-09 04:49

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('System', '0011_destaques'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='LogDPO',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto', models.TextField(max_length=150, null=True, verbose_name='Texto relatorio')),
                ('datatime', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='LogLota',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto', models.TextField(max_length=150, null=True, verbose_name='Texto relatorio')),
                ('datatime', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.AlterField(
            model_name='post',
            name='texto',
            field=models.TextField(max_length=300, null=True, verbose_name='Texto'),
        ),
        migrations.AlterField(
            model_name='treinamentos',
            name='titulo',
            field=models.TextField(max_length=100, null=True),
        ),
        migrations.CreateModel(
            name='DPOBanimento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datatime', models.DateTimeField(default=django.utils.timezone.now)),
                ('resp', models.TextField(max_length=170, null=True)),
                ('banido', models.TextField(max_length=170, null=True)),
                ('fundação', models.IntegerField(default=0)),
                ('motivo', models.TextField(max_length=170, null=True)),
                ('imagem', models.ImageField(upload_to='imagens/')),
                ('solicitante', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='solicitantedpobanimento', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DPORelatório',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datatime', models.DateTimeField(default=django.utils.timezone.now)),
                ('militares', models.IntegerField(default=0)),
                ('fundação', models.IntegerField(default=0)),
                ('motivo', models.TextField(max_length=170, null=True)),
                ('imagem', models.ImageField(upload_to='imagens/')),
                ('solicitante', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='solicitantedpo', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Lota',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datatime', models.DateTimeField(default=django.utils.timezone.now)),
                ('lotador', models.TextField(max_length=170, null=True)),
                ('recruta', models.TextField(max_length=170, null=True)),
                ('imagem', models.ImageField(upload_to='imagens/')),
                ('solicitante', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='solicitantelota', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]