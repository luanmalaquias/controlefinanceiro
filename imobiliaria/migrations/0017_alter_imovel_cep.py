# Generated by Django 4.1.7 on 2023-03-06 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imobiliaria', '0016_alter_imovel_cep'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imovel',
            name='cep',
            field=models.CharField(blank=True, max_length=9, verbose_name='CEP'),
        ),
    ]
