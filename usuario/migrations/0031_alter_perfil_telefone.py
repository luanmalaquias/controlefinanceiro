# Generated by Django 4.1.7 on 2023-03-23 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0030_alter_perfil_data_nascimento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfil',
            name='telefone',
            field=models.CharField(max_length=16, null=True, verbose_name='Telefone para contato'),
        ),
    ]
