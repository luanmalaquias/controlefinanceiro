# Generated by Django 4.1.7 on 2023-02-22 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imobiliaria', '0007_imovel_bairro_imovel_cep_imovel_cidade_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='imovel',
            name='numeroEndereco',
        ),
        migrations.AddField(
            model_name='imovel',
            name='numero',
            field=models.CharField(blank=True, max_length=100, verbose_name='Numero'),
        ),
    ]
