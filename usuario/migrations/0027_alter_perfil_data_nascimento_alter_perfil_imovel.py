# Generated by Django 4.1.7 on 2023-03-10 02:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('imobiliaria', '0017_alter_imovel_cep'),
        ('usuario', '0026_alter_perfil_data_entrada_imovel_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfil',
            name='data_nascimento',
            field=models.DateField(blank=True, max_length=10, null=True, verbose_name='Data de nascimento'),
        ),
        migrations.AlterField(
            model_name='perfil',
            name='imovel',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='imobiliaria.imovel'),
        ),
    ]