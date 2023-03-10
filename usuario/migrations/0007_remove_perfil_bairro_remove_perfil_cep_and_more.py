# Generated by Django 4.1.7 on 2023-02-21 19:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('imobiliaria', '0001_initial'),
        ('usuario', '0006_alter_perfil_options_alter_perfil_managers_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='perfil',
            name='bairro',
        ),
        migrations.RemoveField(
            model_name='perfil',
            name='cep',
        ),
        migrations.RemoveField(
            model_name='perfil',
            name='cidade',
        ),
        migrations.RemoveField(
            model_name='perfil',
            name='endereco',
        ),
        migrations.RemoveField(
            model_name='perfil',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='perfil',
            name='is_staff',
        ),
        migrations.RemoveField(
            model_name='perfil',
            name='numeroEndereco',
        ),
        migrations.RemoveField(
            model_name='perfil',
            name='uf',
        ),
        migrations.AddField(
            model_name='perfil',
            name='imovel',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.PROTECT, to='imobiliaria.imovel'),
            preserve_default=False,
        ),
    ]
