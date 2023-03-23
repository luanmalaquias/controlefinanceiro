# Generated by Django 4.1.7 on 2023-03-23 02:58

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0027_alter_perfil_data_nascimento_alter_perfil_imovel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfil',
            name='cpf',
            field=models.CharField(max_length=14, null=True, validators=[django.core.validators.MinLengthValidator(14)]),
        ),
        migrations.AlterField(
            model_name='perfil',
            name='data_nascimento',
            field=models.DateField(blank=True, max_length=10, null=True, validators=[django.core.validators.MinLengthValidator(16)], verbose_name='Data de nascimento'),
        ),
        migrations.AlterField(
            model_name='perfil',
            name='telefone',
            field=models.CharField(max_length=16, null=True, validators=[django.core.validators.MinLengthValidator(16)], verbose_name='Telefone para contato'),
        ),
    ]