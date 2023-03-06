# Generated by Django 4.1.7 on 2023-03-06 14:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('usuario', '0024_alter_perfil_imovel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfil',
            name='data_entrada_imovel',
            field=models.DateField(blank=True, null=True, verbose_name='Data de entrada no imovel'),
        ),
        migrations.AlterField(
            model_name='perfil',
            name='data_nascimento',
            field=models.DateField(blank=True, max_length=10, null=True, verbose_name='Data de nascimento'),
        ),
        migrations.AlterField(
            model_name='perfil',
            name='telefone',
            field=models.CharField(blank=True, max_length=16, null=True, verbose_name='Telefone para contato'),
        ),
        migrations.AlterField(
            model_name='perfil',
            name='usuario',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
