# Generated by Django 3.1.2 on 2021-05-16 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0011_auto_20210516_0806'),
    ]

    operations = [
        migrations.AddField(
            model_name='sell_list',
            name='status_sell',
            field=models.BooleanField(default=False, verbose_name='Статус исполнения продажи'),
        ),
    ]
