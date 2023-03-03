# Generated by Django 4.1.7 on 2023-02-28 18:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('usuario', '0022_alter_perfil_nome_completo_alter_perfil_telefone_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pagamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=False, verbose_name='Status do pagamento')),
                ('data', models.DateField(verbose_name='Data do pagamento')),
                ('perfil', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='usuario.perfil', verbose_name='Usuario pagador')),
            ],
        ),
    ]