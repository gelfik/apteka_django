# Generated by Django 3.1.2 on 2021-05-15 01:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proizvoditel_list',
            name='address',
        ),
    ]
