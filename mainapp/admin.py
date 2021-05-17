from django.contrib import admin
from .models import *


@admin.register(county_list)
class county_list(admin.ModelAdmin):
    list_display = ('name', 'del_status')


@admin.register(brend_list)
class brend_list(admin.ModelAdmin):
    list_display = ('name', 'del_status')


@admin.register(proizvoditel_list)
class proizvoditel_list(admin.ModelAdmin):
    list_display = ('name', 'country_id', 'zavod_name', 'del_status')


@admin.register(category_preporat_list)
class category_preporat_list(admin.ModelAdmin):
    list_display = ('name', 'del_status')


@admin.register(pod_category_preporat_list)
class pod_category_preporat_list(admin.ModelAdmin):
    list_display = ('name', 'category_preporat_id', 'del_status')


@admin.register(preporat_list)
class preporat_list(admin.ModelAdmin):
    list_display = (
        'name', 'price', 'recept', 'count', 'del_status', 'proizvoditel_id',
        'pod_category_preporat_id', 'brend_id')


@admin.register(postavchiki_list)
class postavchiki_list(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone', 'del_status')


@admin.register(postavki_list)
class postavki_list(admin.ModelAdmin):
    list_display = ('date_postavki', 'total_price', 'total_count', 'postavchiki_id', 'status_postavki', 'del_status')


@admin.register(postavki_element_list)
class postavki_element_list(admin.ModelAdmin):
    list_display = ('preporat_id', 'postavki_id', 'postavka_price', 'count', 'del_status')


@admin.register(sell_list)
class sell_list(admin.ModelAdmin):
    list_display = ('date_time', 'sell_user_id', 'total_price', 'total_count', 'status_sell', 'del_status')


@admin.register(sell_element_list)
class sell_element_list(admin.ModelAdmin):
    list_display = ('preporat_id', 'price', 'count', 'del_status')
