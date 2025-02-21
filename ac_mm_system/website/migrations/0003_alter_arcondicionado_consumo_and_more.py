# Generated by Django 5.1.3 on 2025-02-19 02:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_alter_horario_turno'),
    ]

    operations = [
        migrations.AlterField(
            model_name='arcondicionado',
            name='consumo',
            field=models.FloatField(verbose_name='Consumo'),
        ),
        migrations.AlterField(
            model_name='arcondicionado',
            name='potencia_kw',
            field=models.FloatField(verbose_name='Potência'),
        ),
        migrations.AlterField(
            model_name='arcondicionado',
            name='sala',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ares_condicionados', to='website.sala'),
        ),
        migrations.AlterField(
            model_name='horario',
            name='sala',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='horarios', to='website.sala'),
        ),
        migrations.AlterField(
            model_name='pavilhao',
            name='numero_salas',
            field=models.IntegerField(verbose_name='Número de salas'),
        ),
        migrations.AlterField(
            model_name='sala',
            name='pavilhao',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='salas', to='website.pavilhao'),
        ),
    ]
