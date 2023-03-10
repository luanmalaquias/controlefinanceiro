# Generated by Django 4.1.7 on 2023-02-23 01:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imobiliaria', '0008_remove_imovel_numeroendereco_imovel_numero'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imovel',
            name='mensalidade',
            field=models.CharField(blank=True, max_length=10, verbose_name='Mensalidade R$'),
        ),
        migrations.AlterField(
            model_name='imovel',
            name='vencimento',
            field=models.IntegerField(default=1, verbose_name='Dia do vencimento da mensalidade'),
        ),
    ]
