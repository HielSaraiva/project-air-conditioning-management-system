# Generated by Django 5.1.5 on 2025-05-04 11:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0012_remove_sala_unique_sala_por_pavilhao'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='arcondicionado',
            name='unique_arcondicionado_por_sala',
        ),
    ]
