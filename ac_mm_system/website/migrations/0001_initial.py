# Generated by Django 5.1.3 on 2025-01-28 16:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pavilhao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100, unique=True, verbose_name='Nome')),
                ('numero_salas', models.IntegerField(verbose_name='Numero de salas')),
            ],
        ),
        migrations.CreateModel(
            name='Horario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dias_da_semana', models.CharField(max_length=100)),
                ('horario_inicio', models.TimeField()),
                ('horario_fim', models.TimeField()),
                ('pavilhao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.pavilhao')),
            ],
        ),
        migrations.CreateModel(
            name='Sala',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100, unique=True, verbose_name='Nome')),
                ('horario', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='sala_horario', to='website.horario')),
                ('pavilhao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.pavilhao')),
            ],
        ),
    ]
