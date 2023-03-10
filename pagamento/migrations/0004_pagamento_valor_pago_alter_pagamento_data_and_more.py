# Generated by Django 4.1.7 on 2023-02-28 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pagamento', '0003_alter_pagamento_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='pagamento',
            name='valor_pago',
            field=models.CharField(max_length=10, null=True, verbose_name='Valor pago'),
        ),
        migrations.AlterField(
            model_name='pagamento',
            name='data',
            field=models.DateField(blank=True, verbose_name='Data do pagamento'),
        ),
        migrations.AlterField(
            model_name='pagamento',
            name='status',
            field=models.CharField(choices=[('Concluido', 'Concluido'), ('Nao efetuado', 'Nao efetuado')], default='Nao efetuado', max_length=20, verbose_name='Status do pagamento'),
        ),
    ]
