# Generated by Django 3.2.5 on 2021-08-24 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0009_usuario_updated_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuario',
            name='updated_date',
        ),
        migrations.AlterField(
            model_name='usuario',
            name='foto',
            field=models.ImageField(default='images/icono.png', upload_to='images/'),
        ),
    ]