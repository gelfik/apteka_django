# Generated by Django 3.1.2 on 2021-05-15 04:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0006_auto_20210515_0732'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sell_element_list',
            name='date_time',
        ),
        migrations.RemoveField(
            model_name='sell_element_list',
            name='sell_id',
        ),
        migrations.AlterField(
            model_name='postavki_list',
            name='status_postavki',
            field=models.BooleanField(default=False, verbose_name='Статус выполнения поставки'),
        ),
    ]
