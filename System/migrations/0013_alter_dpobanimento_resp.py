# Generated by Django 5.1.3 on 2024-12-09 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('System', '0012_logdpo_loglota_alter_post_texto_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dpobanimento',
            name='resp',
            field=models.TextField(max_length=170, null=True, verbose_name='Responsável'),
        ),
    ]
