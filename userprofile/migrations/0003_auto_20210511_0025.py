# Generated by Django 3.1.2 on 2021-05-10 21:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0002_auto_20210511_0023'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userprofile',
            options={'permissions': (('add_user', 'Добавление сотрудника'), ('edit_user', 'Редактирвоание сотрудника'), ('delete_user', 'Удаление сотрудника'), ('look_user', 'Просмотр сотрудников')), 'verbose_name': 'Пользователь', 'verbose_name_plural': 'Пользователи'},
        ),
    ]