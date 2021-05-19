from django.forms import ModelForm
from django.utils import timezone
from .models import *
from django import forms
from django.utils.translation import gettext, gettext_lazy as _
import datetime


# Create the form class.

class DateInput(forms.DateInput):
    input_type = 'date'

class brend_Form(ModelForm):
    name = forms.CharField(label=_("Название бренда"), widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = brend_list
        fields = ['name']


class proizvoditel_Form(ModelForm):
    name = forms.CharField(label=_("Название производителя"), widget=forms.TextInput(attrs={'class': 'form-control'}))
    zavod_name = forms.CharField(label=_("Завод-производитель"),
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))
    country_id = forms.ModelChoiceField(label=_("Страна"), widget=forms.Select(attrs={'class': 'form-control'}),
                                        queryset=None)

    class Meta:
        model = proizvoditel_list
        fields = ['name', 'zavod_name', 'country_id']

    def __init__(self, *args, **kwargs):
        super(proizvoditel_Form, self).__init__(*args, **kwargs)
        self.fields['country_id'].queryset = county_list.objects.all().filter(del_status=1)


class category_preporat_Form(ModelForm):
    name = forms.CharField(label=_("Название категории"), widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = category_preporat_list
        fields = ['name']


class pod_category_preporat_Form(ModelForm):
    name = forms.CharField(label=_("Название подкатегории"), widget=forms.TextInput(attrs={'class': 'form-control'}))
    category_preporat_id = forms.ModelChoiceField(label=_("Категория"),
                                                  widget=forms.Select(attrs={'class': 'form-control'}), queryset=None)

    class Meta:
        model = pod_category_preporat_list
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super(pod_category_preporat_Form, self).__init__(*args, **kwargs)
        self.fields['category_preporat_id'].queryset = category_preporat_list.objects.all().filter(del_status=1)
        del self.fields['category_preporat_id']

    def save(self, commit=True, category_id=0):
        data = super(pod_category_preporat_Form, self).save(commit=False)
        data.category_preporat_id = category_preporat_list.objects.get(id=category_id)
        if commit:
            data.save()
        return data


class preporat_Form(ModelForm):
    name = forms.CharField(label=_("Название препората"), widget=forms.TextInput(attrs={'class': 'form-control'}))
    proizvoditel_id = forms.ModelChoiceField(label=_("Производитель"),
                                             widget=forms.Select(attrs={'class': 'form-control'}), queryset=None)
    pod_category_preporat_id = forms.ModelChoiceField(label=_("Подкатегория"),
                                                      widget=forms.Select(attrs={'class': 'form-control'}),
                                                      queryset=None)
    brend_id = forms.ModelChoiceField(label=_("Брэнд"), widget=forms.Select(attrs={'class': 'form-control'}),
                                      queryset=None)
    price = forms.FloatField(label=_("Цена"), widget=forms.NumberInput(attrs={'class': 'form-control'}))
    recept = forms.BooleanField(label=_("Нужен рецепт?"), widget=forms.CheckboxInput(attrs={'class': 'form-control'}),
                                required=False)

    class Meta:
        model = preporat_list
        fields = ['name', 'proizvoditel_id', 'pod_category_preporat_id', 'brend_id', 'price', 'recept']

    def __init__(self, *args, **kwargs):
        super(preporat_Form, self).__init__(*args, **kwargs)
        self.fields['proizvoditel_id'].queryset = proizvoditel_list.objects.all().filter(del_status=1)
        self.fields['pod_category_preporat_id'].queryset = pod_category_preporat_list.objects.all().filter(del_status=1)
        self.fields['brend_id'].queryset = brend_list.objects.all().filter(del_status=1)


class postavchiki_Form(ModelForm):
    name = forms.CharField(label=_("Название поставщика"), widget=forms.TextInput(attrs={'class': 'form-control'}))
    address = forms.CharField(label=_("Адрес поставщика"), widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(label=_("Телефон поставщика"), widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = postavchiki_list
        fields = ['name', 'address', 'phone']


class postavki_Form(ModelForm):
    date_postavki = forms.DateField(label=_("Дата и время поставки"),
                                    widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    total_price = forms.FloatField(label=_("Итоговая стоимость"),
                                   widget=forms.NumberInput(attrs={'class': 'form-control'}))
    total_count = forms.IntegerField(label=_("Общее кол-во товаров"),
                                     widget=forms.NumberInput(attrs={'class': 'form-control'}))
    postavchiki_id = forms.ModelChoiceField(label=_("Поставщик"), widget=forms.Select(attrs={'class': 'form-control'}),
                                            queryset=None)
    status_postavki = forms.BooleanField(label=_("Статус выполнения поставки"),
                                         widget=forms.CheckboxInput(attrs={'class': 'form-control'}),
                                         required=False)

    class Meta:
        model = postavki_list
        fields = ['total_price', 'date_postavki', 'total_count', 'postavchiki_id', 'status_postavki']

    def __init__(self, *args, **kwargs):
        super(postavki_Form, self).__init__(*args, **kwargs)
        self.fields['postavchiki_id'].queryset = postavchiki_list.objects.all().filter(del_status=1)
        del self.fields['total_price']
        del self.fields['total_count']
        del self.fields['status_postavki']

    # def save(self, commit=True):
    #     data_inf = super(postavki_Form, self).save(commit=False)
    #     if commit:
    #         data_inf.save()
    #     return data_inf


class postavki_element_Form(ModelForm):
    preporat_id = forms.ModelChoiceField(label=_("Препорат"), widget=forms.Select(attrs={'class': 'form-control'}),
                                         queryset=None)
    postavki_id = forms.ModelChoiceField(label=_("Поставка"), widget=forms.Select(attrs={'class': 'form-control'}),
                                         queryset=None)
    postavka_price = forms.FloatField(label=_("Закупочная стоимость"),
                                      widget=forms.NumberInput(attrs={'class': 'form-control'}))
    count = forms.IntegerField(label=_("Количество"), widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = postavki_element_list
        fields = ['preporat_id', 'postavka_price', 'count']

    def __init__(self, *args, **kwargs):
        super(postavki_element_Form, self).__init__(*args, **kwargs)
        self.fields['preporat_id'].queryset = preporat_list.objects.all().filter(del_status=1)
        self.fields['postavki_id'].queryset = postavki_list.objects.all().filter(del_status=1)
        del self.fields['postavki_id']

    def save(self, commit=True, postavki_id=0):
        data = super(postavki_element_Form, self).save(commit=False)
        data.postavki_id = postavki_list.objects.get(id=postavki_id)
        if commit:
            data.save()
        return data


class sell_Form(ModelForm):
    # date_time = forms.DateTimeField(label=_("Дата и время продажи"),
    #                                 widget=forms.DateTimeInput(attrs={'class': 'form-control'}))
    sell_user_id = forms.ModelChoiceField(label=_("Продавец"), widget=forms.Select(attrs={'class': 'form-control'}),
                                          queryset=None)
    total_price = forms.FloatField(label=_("Итоговая стоимость"),
                                   widget=forms.NumberInput(attrs={'class': 'form-control'}))
    total_count = forms.IntegerField(label=_("Итоговое количество"),
                                     widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = sell_list
        fields = ['sell_user_id', 'total_price', 'total_count']

    def __init__(self, *args, **kwargs):
        super(sell_Form, self).__init__(*args, **kwargs)
        self.fields['sell_user_id'].queryset = User.objects.all().filter(del_status=1)
        # del self.fields['date_time']
        del self.fields['sell_user_id']
        del self.fields['total_price']
        del self.fields['total_count']


class sell_element_Form(ModelForm):
    preporat_id = forms.ModelChoiceField(label=_("Препорат"), widget=forms.Select(attrs={'class': 'form-control'}),
                                         queryset=None)
    sell_id = forms.ModelChoiceField(label=_("Продажа"), widget=forms.Select(attrs={'class': 'form-control'}),
                                     queryset=None)
    price = forms.FloatField(label=_("Цена"),
                             widget=forms.NumberInput(attrs={'class': 'form-control'}))
    count = forms.IntegerField(label=_("Количество"), widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = sell_element_list
        fields = ['preporat_id', 'sell_id', 'price', 'count']

    def __init__(self, *args, **kwargs):
        super(sell_element_Form, self).__init__(*args, **kwargs)
        self.fields['preporat_id'].queryset = preporat_list.objects.all().filter(del_status=1)
        self.fields['sell_id'].queryset = sell_list.objects.all().filter(del_status=1)
        del self.fields['sell_id']
        del self.fields['price']

    def save(self, commit=True, sell_id=0, price=0):
        data = super(sell_element_Form, self).save(commit=False)
        data.sell_id = sell_list.objects.get(id=sell_id)
        data.price = price
        if commit:
            data.save()
        return data
