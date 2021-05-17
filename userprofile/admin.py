# -*- coding:utf-8 -*-
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserProfile

class UserInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Доп. информация'

    fields = ('patronymic', 'birthday', 'phone')

# Определяем новый класс настроек для модели User
class UserAdmin(UserAdmin):
    inlines = (UserInline,)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (('Первональная информация'), {'fields': ('first_name', 'last_name', 'email')}),
        (('Права доступа'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (('Группы'), {'fields': ('groups',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'first_name', 'last_name', 'email')}
         ),
    )
    list_display = ('last_name', 'username', 'last_name', 'first_name', 'email', 'is_staff')
    list_select_related = ('userprofile',)

    readonly_fields = [
        'last_login',
        'date_joined',
    ]
    #
    # # def get_role(self, instance):
    # #     return instance.userprofile.role
    # #
    # # get_role.short_description = 'Роль'


# Перерегистрируем модель User
admin.site.unregister(User)
admin.site.register(User, UserAdmin)