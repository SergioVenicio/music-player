# Generated by Django 3.0.2 on 2020-11-02 17:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='like',
            table='like',
        ),
        migrations.AlterModelTable(
            name='user',
            table='user',
        ),
    ]
