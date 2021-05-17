import django
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
from django.utils import timezone


class county_list(models.Model):
    name = models.CharField('Название страны', max_length=256, default=None, unique=True)
    del_status = models.BooleanField('Статус удаления', default=True)

    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'
        db_table = 'countries'

    def __str__(self):
        return self.name


class brend_list(models.Model):
    name = models.CharField('Название бренда', max_length=256, default=None, unique=True)
    del_status = models.BooleanField('Статус удаления', default=True)

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'
        db_table = 'brends'

    def __str__(self):
        return self.name


class proizvoditel_list(models.Model):
    name = models.CharField('Название производителя', max_length=256, default=None, unique=True)
    zavod_name = models.CharField('Завод-производитель', max_length=256, default=None)
    country_id = models.ForeignKey(county_list, on_delete=models.CASCADE, verbose_name='Страна производителя',
                                   default=None)
    del_status = models.BooleanField('Статус удаления', default=True)

    class Meta:
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производители'
        db_table = 'proizvoditels'

    def __str__(self):
        return self.name


class category_preporat_list(models.Model):
    name = models.CharField('Название категории', max_length=256, default=None, unique=True)
    del_status = models.BooleanField('Статус удаления', default=True)

    class Meta:
        verbose_name = 'Категория препората'
        verbose_name_plural = 'Категории препоратов'
        db_table = 'category_preporat'

    def __str__(self):
        return self.name


class pod_category_preporat_list(models.Model):
    name = models.CharField('Название подкатегории', max_length=256, default=None, unique=True)
    category_preporat_id = models.ForeignKey(category_preporat_list, on_delete=models.CASCADE, verbose_name='Категория',
                                             default=None)
    del_status = models.BooleanField('Статус удаления', default=True)

    class Meta:
        verbose_name = 'Подкатегория препората'
        verbose_name_plural = 'Подкатегории препоратов'
        db_table = 'pod_category_preporat'

    def __str__(self):
        return self.name


class preporat_list(models.Model):
    name = models.CharField('Название препората', max_length=256, default=None)
    proizvoditel_id = models.ForeignKey(proizvoditel_list, on_delete=models.CASCADE, verbose_name='Производитель',
                                        default=None)
    pod_category_preporat_id = models.ForeignKey(pod_category_preporat_list, on_delete=models.CASCADE,
                                                 verbose_name='Подкатегория',
                                                 default=None)
    brend_id = models.ForeignKey(brend_list, on_delete=models.CASCADE, verbose_name='Брэнд',
                                 default=None)
    price = models.FloatField('Цена', default=0)
    count = models.IntegerField('Кол-во препората в наличии', default=0)
    recept = models.BooleanField('Требование рецепта', default=False)
    del_status = models.BooleanField('Статус удаления', default=True)

    class Meta:
        verbose_name = 'Препорат'
        verbose_name_plural = 'Препораты'
        db_table = 'preporats'

    def __str__(self):
        return str(self.name)


class postavchiki_list(models.Model):
    name = models.CharField('Название поставщика', max_length=256, default=None)
    address = models.TextField('Адрес поставщика', default=None)
    phone = models.CharField('Телефон поставщика', max_length=32, null=True)
    del_status = models.BooleanField('Статус удаления', default=True)

    class Meta:
        verbose_name = 'Поставщик'
        verbose_name_plural = 'Поставщики'
        db_table = 'postavchiki'

    def __str__(self):
        return self.name


class postavki_list(models.Model):
    date_postavki = models.DateField('Дата поставки', default=None)
    total_price = models.FloatField('Итоговая стоимость', default=0)
    total_count = models.IntegerField('Общее кол-во товаров', default=0)
    postavchiki_id = models.ForeignKey(postavchiki_list, on_delete=models.CASCADE, verbose_name='Поставщик',
                                       default=None)
    status_postavki = models.BooleanField('Статус выполнения поставки', default=False)
    del_status = models.BooleanField('Статус удаления', default=True)

    class Meta:
        verbose_name = 'Поставка'
        verbose_name_plural = 'Поставки'
        db_table = 'postavki'

    def __str__(self):
        return str(self.date_postavki)


class postavki_element_list(models.Model):
    preporat_id = models.ForeignKey(preporat_list, on_delete=models.CASCADE, verbose_name='Препорат',
                                    default=None)
    postavki_id = models.ForeignKey(postavki_list, on_delete=models.CASCADE, verbose_name='Поставка',
                                    default=None)
    postavka_price = models.FloatField('Закупочная стоимость', default=0)
    count = models.IntegerField('Колличество', default=0)
    del_status = models.BooleanField('Статус удаления', default=True)

    class Meta:
        verbose_name = 'Поставки товар'
        verbose_name_plural = 'Поставки товары'
        db_table = 'postavki_element'

    def __str__(self):
        return str(self.preporat_id)


class sell_list(models.Model):
    # date_time = models.DateTimeField('Дата и время продажи', default=None)
    date_time = models.DateTimeField('Дата и время продажи', auto_now_add=True)
    sell_user_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Продавец',
                                     default=None)
    total_price = models.FloatField('Итоговая стоимость', default=0)
    total_count = models.IntegerField('Итоговое колличество', default=0)
    status_sell = models.BooleanField('Статус исполнения продажи', default=False)
    del_status = models.BooleanField('Статус удаления', default=True)

    class Meta:
        verbose_name = 'Продажа'
        verbose_name_plural = 'Продажи'
        db_table = 'sell'

    def __str__(self):
        return str(self.date_time)


class sell_element_list(models.Model):
    preporat_id = models.ForeignKey(preporat_list, on_delete=models.CASCADE, verbose_name='Препорат',
                                    default=None)
    sell_id = models.ForeignKey(sell_list, on_delete=models.CASCADE, verbose_name='Продажа',
                                default=None)
    price = models.FloatField('Итоговая стоимость', default=0)
    count = models.IntegerField('Колличество', default=0)
    del_status = models.BooleanField('Статус удаления', default=True)

    class Meta:
        verbose_name = 'Продажа элемент'
        verbose_name_plural = 'Продажи элементы'
        db_table = 'sell_element'

    def __str__(self):
        return f'{self.preporat_id} {self.price}р. {self.count}'
