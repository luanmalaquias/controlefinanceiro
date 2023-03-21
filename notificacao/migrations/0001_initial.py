# Generated by Django 4.1.7 on 2023-03-20 18:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('usuario', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notificacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datahora', models.DateTimeField(auto_now_add=True, verbose_name='Data/hora da notificacao')),
                ('mensagem', models.TextField(verbose_name='Mensagem')),
                ('lido', models.BooleanField(default=False, verbose_name='Notificação lida?')),
                ('resolvido', models.BooleanField(default=False, verbose_name='Problema resolvido?')),
                ('perfil', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuario.perfil', verbose_name='Usuario')),
            ],
        ),
    ]