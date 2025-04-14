# Generated by Django 5.1.5 on 2025-04-14 02:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0008_alter_pavilhao_nome_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sala',
            name='nome',
            field=models.CharField(max_length=100, verbose_name='Nome'),
        ),
        migrations.AddConstraint(
            model_name='arcondicionado',
            constraint=models.UniqueConstraint(fields=('sala', 'nome'), name='unique_arcondicionado_por_sala'),
        ),
        migrations.AddConstraint(
            model_name='sala',
            constraint=models.UniqueConstraint(fields=('pavilhao', 'nome'), name='unique_sala_por_pavilhao'),
        ),
    ]
