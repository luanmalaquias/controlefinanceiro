# Generated by Django 4.1.7 on 2023-03-13 00:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pagamento', '0015_alter_pagamento_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pagamento',
            name='data',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Data do pagamento'),
        ),
    ]
