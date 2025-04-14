# Generated by Django 5.1.5 on 2025-04-13 21:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_alter_grafico_usuario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grafico',
            name='valor_kWh',
            field=models.FloatField(default=0.0, verbose_name='Valor em R$ por kWh'),
        ),
    ]
