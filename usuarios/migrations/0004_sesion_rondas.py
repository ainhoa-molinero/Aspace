# Generated by Django 3.2.5 on 2021-08-13 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0003_alter_sesion_fichero'),
    ]

    operations = [
        migrations.AddField(
            model_name='sesion',
            name='rondas',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
