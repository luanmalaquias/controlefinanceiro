# Generated by Django 4.1.7 on 2023-02-27 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0019_alter_perfil_data_entrada_imovel'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfil',
            name='data_nascimento',
            field=models.DateField(null=True, verbose_name='Data de nascimento do usuario'),
        ),
    ]
