# Generated by Django 5.1.3 on 2024-12-01 00:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('System', '0007_alter_logtimeline_requerimento_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logtimeline',
            name='requerimento',
            field=models.CharField(choices=[('Promoção', 'Promoção'), ('Rebaixamento', 'Rebaixamento'), ('Advertência', 'Advertência'), ('Demissão', 'Demissão'), ('Banimento', 'Banimento'), ('Treinamento', 'Treinamento')], max_length=50, null=True, verbose_name='Tipo'),
        ),
        migrations.AlterField(
            model_name='requerimento',
            name='requerimento',
            field=models.CharField(choices=[('Promoção', 'Promoção'), ('Rebaixamento', 'Rebaixamento'), ('Advertência', 'Advertência'), ('Demissão', 'Demissão'), ('Banimento', 'Banimento'), ('Treinamento', 'Treinamento')], max_length=50, null=True, verbose_name='Tipo'),
        ),
    ]