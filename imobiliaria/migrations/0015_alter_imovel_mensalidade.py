# Generated by Django 4.1.7 on 2023-02-28 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imobiliaria', '0014_remove_imovel_mensalidade2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imovel',
            name='mensalidade',
            field=models.CharField(blank=True, max_length=10, verbose_name='Mensalidade R$'),
        ),
    ]
