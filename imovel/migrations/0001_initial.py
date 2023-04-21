# Generated by Django 4.2 on 2023-04-13 17:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('locador', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Imovel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(help_text='Nome do imóvel / vila / condominio', max_length=50)),
                ('numero', models.CharField(max_length=100)),
                ('cep', models.CharField(max_length=9)),
                ('endereco', models.CharField(max_length=100)),
                ('bairro', models.CharField(max_length=100)),
                ('cidade', models.CharField(max_length=100)),
                ('uf', models.CharField(max_length=2)),
                ('mensalidade', models.CharField(max_length=10)),
                ('disponivel', models.BooleanField(default=True)),
                ('locador', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='locador.locador')),
            ],
        ),
    ]