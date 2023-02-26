# Generated by Django 4.1.7 on 2023-02-21 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imobiliaria', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='imovel',
            name='mensalidade',
            field=models.FloatField(blank=True, default=0.0, verbose_name='Mensalidade'),
        ),
        migrations.AlterField(
            model_name='imovel',
            name='nome',
            field=models.CharField(blank=True, max_length=50, verbose_name='Nome do imóvel / vila / condominio'),
        ),
    ]