# Generated by Django 4.1.7 on 2023-03-02 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pagamento', '0011_alter_pagamento_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pagamento',
            name='status',
            field=models.CharField(choices=[('P', 'Pago'), ('A', 'Em Análise')], default='A', max_length=20, verbose_name='Status do pagamento'),
        ),
    ]
