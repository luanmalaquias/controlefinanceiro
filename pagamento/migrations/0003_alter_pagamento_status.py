# Generated by Django 4.1.7 on 2023-02-28 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pagamento', '0002_alter_pagamento_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pagamento',
            name='status',
            field=models.CharField(choices=[('Concluido', 'Concluido'), ('Nao efetuado', 'Nao efetuado')], max_length=20, verbose_name='Status do pagamento'),
        ),
    ]
