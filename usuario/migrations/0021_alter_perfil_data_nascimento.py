# Generated by Django 4.1.7 on 2023-02-27 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0020_perfil_data_nascimento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfil',
            name='data_nascimento',
            field=models.DateField(max_length=10, null=True, verbose_name='Data de nascimento'),
        ),
    ]