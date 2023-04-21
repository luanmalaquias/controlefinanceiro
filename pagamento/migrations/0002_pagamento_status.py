# Generated by Django 4.2 on 2023-04-20 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pagamento', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pagamento',
            name='status',
            field=models.CharField(choices=[('P', 'Pago'), ('A', 'Em Análise'), ('N', 'Não pago')], default='A', max_length=20, verbose_name='Status do pagamento'),
        ),
    ]