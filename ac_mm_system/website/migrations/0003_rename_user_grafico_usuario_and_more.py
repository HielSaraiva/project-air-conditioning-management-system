# Generated by Django 5.1.5 on 2025-04-12 21:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_grafico_user_pavilhao_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='grafico',
            old_name='user',
            new_name='usuario',
        ),
        migrations.RenameField(
            model_name='pavilhao',
            old_name='user',
            new_name='usuario',
        ),
    ]
