# Generated by Django 5.1.3 on 2024-12-10 01:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('System', '0013_alter_dpobanimento_resp'),
    ]

    operations = [
        migrations.AddField(
            model_name='dporelatório',
            name='base',
            field=models.CharField(choices=[('Abertura', 'Abertura'), ('Pausa', 'Pausa'), ('Fechamento', 'Fechamento')], max_length=50, null=True),
        ),
    ]
