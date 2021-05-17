# -*- coding:utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    patronymic = models.CharField('Отчество', max_length=32, null=True, blank=False)
    password = models.CharField(max_length=256, null=True, blank=True)
    birthday = models.DateField('Дата рождения', null=True, blank=False)
    phone = models.CharField('Телефон', max_length=32, null=True, blank=False)

    def __unicode__(self):
        return self.user

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

        permissions = (
            # Идентификатор права       Описание права
            ("look_user", "Просмотр сотрудников"),
        )


# @receiver(post_save, sender=User)
# def new_user(sender, instance, created, **kwargs):
#     if created:
#         UserProfile.objects.create(user=instance)
#         instance.userprofile.save()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()
