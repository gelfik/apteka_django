# -*- coding: utf-8 -*-
import os

import xhtml2pdf
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View

from apteka_django import settings
from .forms import *
from django.template.context_processors import csrf
from django.contrib.auth.models import User, Group
from django.contrib import auth
from django.db.models import Sum

# from django_xhtml2pdf.utils import pdf_decorator

from io import BytesIO, StringIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa


def fetch_pdf_resources(uri, rel):
    if uri.find(settings.MEDIA_URL) != -1:
        path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ''))
    elif uri.find(settings.STATIC_URL) != -1:
        path = os.path.join(settings.STATIC_ROOT, uri.replace(settings.STATIC_URL, ''))
    else:
        path = None
    print(path)
    return path


def render_pdf(url_template, context):
    template = get_template(url_template)
    html = template.render(context)

    result = BytesIO()
    # result = StringIO()
    pdf = pisa.CreatePDF(BytesIO(html.encode('utf-8')), result,
                         encode='utf-8',
                         link_callback=fetch_pdf_resources)

    print(result)
    # print(b'\x93'.decode('utf-8'))
    print(result.getvalue())
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type="application/pdf")
    return None

# @pdf_decorator
def pdf_get(request):
    arguments = {}
    arguments.update(csrf(request))
    if request.method == "GET":
        if request.user.is_authenticated:
            try:
                arguments.update(data_search=preporat_list.objects.all().filter(del_status=1))
            except:
                pass
            if has_group(request.user, 'Фармацевт'):
                return render(request, 'mainapp/admin/pdf_preports.html', {'arguments': arguments})
            elif has_group(request.user, 'Администратор'):
                # return render(request, 'mainapp/admin/preporat_list.html', {'arguments': arguments})
                # return HttpResponse(render(request, 'mainapp/admin/pdf_preports.html', {'arguments': arguments}), content_type="application/pdf")
                pdf = render_pdf("mainapp/admin/pdf_preports.html", context={'arguments': arguments, 'request': request, 'user': request.user})
                return HttpResponse(pdf, content_type="application/pdf")
            else:
                auth.logout(request)
                return redirect('/')
        else:
            response = render(request, 'mainapp/index.html')
            return response
    else:
        return HttpResponse('405 Method Not Allowed', status=405)


class User_data:
    error_message = ''
    error_status = False
    user = None

    def __init__(self):
        self.user = None

    def set_user(self, user):
        self.user = user

    def set_error(self, error_message):
        self.error_message = error_message
        self.error_status = True

    def get_error(self):
        self.error_status = False
        return f'{self.error_message}'

    def get_error_status(self):
        return self.error_status


usr = User_data()


def has_group(user, group_name):
    from django.contrib.auth.models import Group
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False


def get_int(value):
    try:
        return int(value)
    except:
        return -1


def update_postavka_item(postavka_id):
    data = postavki_element_list.objects.filter(del_status=1, postavki_id=postavka_id)
    item = data.aggregate(Sum('count'))
    postavka_price = 0
    for i, items in enumerate(data):
        postavka_price += items.postavka_price * items.count
    postavka_object = postavki_list.objects.get(id=postavka_id)
    if item['count__sum'] == None or item['count__sum'] == 0:
        postavka_object.total_count = 0
        postavka_object.total_price = 0
    else:
        postavka_object.total_count = item['count__sum']
        postavka_object.total_price = round(postavka_price, 3)
    postavka_object.save()


def update_sell_item(sell_id):
    data = sell_element_list.objects.filter(del_status=1, sell_id=sell_id)
    item = data.aggregate(Sum('count'))
    sell_price = 0
    for i, items in enumerate(data):
        sell_price += items.price * items.count
    sell_object = sell_list.objects.get(id=sell_id)
    if item['count__sum'] == None or item['count__sum'] == 0:
        sell_object.total_count = 0
        sell_object.total_price = 0
    else:
        sell_object.total_count = item['count__sum']
        sell_object.total_price = round(sell_price, 3)
    sell_object.save()


def index(request):
    arguments = {}
    arguments.update(csrf(request))
    if request.method == "GET":
        if request.user.is_authenticated:
            if has_group(request.user, 'Фармацевт'):
                return redirect('/app')
            elif has_group(request.user, 'Администратор'):
                return redirect('/app')
            else:
                auth.logout(request)
                return redirect('/')
        else:
            response = render(request, 'mainapp/index.html')
            return response
    else:
        return HttpResponse('405 Method Not Allowed', status=405)


def login(request):
    arguments = {}
    arguments.update(csrf(request))
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        userdata = auth.authenticate(username=username, password=password)
        try:
            usersearch = User.objects.get(username=username)
        except:
            usersearch = None
        if userdata is not None:
            auth.login(request, userdata)
            usr.set_user(usersearch)
            return redirect('/')
        elif usersearch is not None:
            arguments.update(login_error='Не верный пароль!')
            return render(request, 'mainapp/index.html', {'arguments': arguments})
        else:
            arguments.update(login_error='Пользователь не найден!')
            return render(request, 'mainapp/index.html', {'arguments': arguments})
    else:
        return HttpResponse('405 Method Not Allowed', status=405)


def logout(request):
    auth.logout(request)
    usr.set_user(None)
    return redirect('/')


def app(request):
    arguments = {}
    if request.user.is_authenticated:
        if request.method == "GET":
            if has_group(request.user, 'Фармацевт'):
                return redirect('/app/sell/')
                # return render(request, 'mainapp/admin/index.html', {'arguments': arguments})
            elif has_group(request.user, 'Администратор'):
                return redirect('/app/sell/')
                # return render(request, 'mainapp/farmac/index.html', {'arguments': arguments})
            else:
                auth.logout(request)
                return redirect('/')
        else:
            return HttpResponse('405 Method Not Allowed', status=405)
    return redirect('/')


def postavchiki(request):
    arguments = {}
    arguments.update(form=postavchiki_Form)
    arguments.update(postavchiki=postavchiki_list.objects.all().filter(del_status=1))
    postav = []
    for i, item in enumerate(postavchiki_list.objects.all().filter(del_status=1)):
        postav.append({'form': postavchiki_Form(instance=item), 'id': item.id})

    arguments.update(postavchiki_edit=postav)
    if request.user.is_authenticated and has_group(request.user, 'Администратор'):
        if request.method == "GET":
            return render(request, 'mainapp/admin/postavchiki_list.html', {'arguments': arguments})
        elif request.method == "POST":
            newppostavchiki_form = postavchiki_Form(request.POST)
            if newppostavchiki_form.is_valid():
                newppostavchiki_form.save()
                return render(request, 'mainapp/admin/postavchiki_list.html', {'arguments': arguments})
            else:
                arguments.update(error="Форма добавления заполнена не корректно!")
                arguments.update(form=newppostavchiki_form)
                return render(request, 'mainapp/admin/postavchiki_list.html', {'arguments': arguments})
        else:
            return HttpResponse('405 Method Not Allowed', status=405)
    return redirect('/')


def postavchiki_updater(request, postavchik_id):
    arguments = {}
    if request.user.is_authenticated and has_group(request.user, 'Администратор'):
        if request.method == "GET":
            try:
                postavchik_object = postavchiki_list.objects.get(id=postavchik_id)
                postavchik_object.del_status = 0
                postavchik_object.save()
            except:
                pass
            return_url = request.META.get('HTTP_REFERER').split(f'{request.META.get("HTTP_HOST")}')[1]
            return redirect(f'{return_url}')
        elif request.method == "POST":
            try:
                postavchik_object = postavchiki_list.objects.get(id=postavchik_id)
                newppostavchiki_form = postavchiki_Form(request.POST)
                if newppostavchiki_form.is_valid():
                    postavchik_object.name = newppostavchiki_form.cleaned_data.get('name')
                    postavchik_object.address = newppostavchiki_form.cleaned_data.get('address')
                    postavchik_object.phone = newppostavchiki_form.cleaned_data.get('phone')
                postavchik_object.save()
            except:
                pass
            return_url = request.META.get('HTTP_REFERER').split(f'{request.META.get("HTTP_HOST")}')[1]
            return redirect(f'{return_url}')
        else:
            return HttpResponse('405 Method Not Allowed', status=405)
    return redirect('/')


def brends(request):
    arguments = {}
    arguments.update(name_tag=['бренд', 'Бренды', 'брендов', 'бренда'])
    arguments.update(form=brend_Form)
    arguments.update(data_search=brend_list.objects.all().filter(del_status=1))
    data = []
    for i, item in enumerate(arguments['data_search']):
        data.append({'form': brend_Form(instance=item), 'id': item.id})
    arguments.update(data_edit=data)
    if request.user.is_authenticated and has_group(request.user, 'Администратор'):
        if request.method == "GET":
            return render(request, 'mainapp/admin/brends_list.html', {'arguments': arguments})
        elif request.method == "POST":
            newdata_form = brend_Form(request.POST)
            if newdata_form.is_valid():
                newdata_form.save()
                return_url = request.META.get('HTTP_REFERER').split(f'{request.META.get("HTTP_HOST")}')[1]
                return redirect(f'{return_url}')
            else:
                arguments.update(error="Форма добавления заполнена не корректно!")
                arguments.update(form=newdata_form)
                return render(request, 'mainapp/admin/brends_list.html', {'arguments': arguments})
        else:
            return HttpResponse('405 Method Not Allowed', status=405)
    return redirect('/')


def brends_updater(request, id):
    arguments = {}
    if request.user.is_authenticated and has_group(request.user, 'Администратор'):
        if request.method == "GET":
            try:
                data_object = brend_list.objects.get(id=id)
                data_object.del_status = 0
                data_object.save()
            except:
                pass
            return_url = request.META.get('HTTP_REFERER').split(f'{request.META.get("HTTP_HOST")}')[1]
            return redirect(f'{return_url}')
        elif request.method == "POST":
            try:
                data_object = brend_list.objects.get(id=id)
                newp_form = brend_Form(request.POST)
                if newp_form.is_valid():
                    data_object.name = newp_form.cleaned_data.get('name')
                data_object.save()
            except:
                pass
            return_url = request.META.get('HTTP_REFERER').split(f'{request.META.get("HTTP_HOST")}')[1]
            return redirect(f'{return_url}')
        else:
            return HttpResponse('405 Method Not Allowed', status=405)
    return redirect('/')


def category(request):
    arguments = {}
    arguments.update(name_tag=['категорию', 'Категории', 'категорий', 'категории'])
    arguments.update(form=category_preporat_Form)
    arguments.update(data_search=category_preporat_list.objects.all().filter(del_status=1))
    if request.user.is_authenticated and has_group(request.user, 'Администратор'):
        if request.method == "GET":
            return render(request, 'mainapp/admin/category_list.html', {'arguments': arguments})
        elif request.method == "POST":
            newdata_form = category_preporat_Form(request.POST)
            if newdata_form.is_valid():
                newdata_form.save()
                return_url = request.META.get('HTTP_REFERER').split(f'{request.META.get("HTTP_HOST")}')[1]
                return redirect(f'{return_url}')
            else:
                arguments.update(error="Форма добавления заполнена не корректно!")
                arguments.update(form=newdata_form)
                return render(request, 'mainapp/admin/category_list.html', {'arguments': arguments})
        else:
            return HttpResponse('405 Method Not Allowed', status=405)
    return redirect('/')


def category_updater(request, id):
    arguments = {}
    if request.user.is_authenticated and has_group(request.user, 'Администратор'):
        if request.method == "GET":
            try:
                data_object = category_preporat_list.objects.get(id=id)
                data_object.del_status = 0
                data_object.save()
            except:
                pass
            return_url = request.META.get('HTTP_REFERER').split(f'{request.META.get("HTTP_HOST")}')[1]
            return redirect(f'{return_url}')
        elif request.method == "POST":
            try:
                data_object = category_preporat_list.objects.get(id=id)
                newp_form = category_preporat_Form(request.POST)
                if newp_form.is_valid():
                    data_object.name = newp_form.cleaned_data.get('name')
                data_object.save()
            except:
                pass
            return_url = request.META.get('HTTP_REFERER').split(f'{request.META.get("HTTP_HOST")}')[1]
            return redirect(f'{return_url}')
        else:
            return HttpResponse('405 Method Not Allowed', status=405)
    return redirect('/')


def podcategory(request, category_id):
    arguments = {}
    arguments.update(name_tag=['подкатегорию', 'Подкатегории', 'подкатегорий', 'подкатегории', 'категорию'])
    arguments.update(form=pod_category_preporat_Form)
    arguments.update(
        data_search=pod_category_preporat_list.objects.all().filter(del_status=1, category_preporat_id=category_id))
    data = []
    for i, item in enumerate(arguments['data_search']):
        data.append({'form': pod_category_preporat_Form(instance=item), 'id': item.id})
    arguments.update(data_edit=data)
    arguments.update(category=category_preporat_list.objects.get(del_status=1, id=category_id))
    arguments.update(form_category=category_preporat_Form(instance=arguments['category']))

    if request.user.is_authenticated and has_group(request.user, 'Администратор'):
        if request.method == "GET":
            return render(request, 'mainapp/admin/podcategory_list.html', {'arguments': arguments})
        elif request.method == "POST":
            newdata_form = pod_category_preporat_Form(request.POST)
            if newdata_form.is_valid():
                newdata_form.save(category_id=category_id)
                return_url = request.META.get('HTTP_REFERER').split(f'{request.META.get("HTTP_HOST")}')[1]
                return redirect(f'{return_url}')
            else:
                arguments.update(error="Форма добавления заполнена не корректно!")
                arguments.update(form=newdata_form)
                return render(request, 'mainapp/admin/podcategory_list.html', {'arguments': arguments})
        else:
            return HttpResponse('405 Method Not Allowed', status=405)
    return redirect('/')


def podcategory_updater(request, category_id, id):
    arguments = {}
    if request.user.is_authenticated and has_group(request.user, 'Администратор'):
        if request.method == "GET":
            try:
                data_object = pod_category_preporat_list.objects.get(id=id)
                data_object.del_status = 0
                data_object.save()
            except:
                pass
            return_url = request.META.get('HTTP_REFERER').split(f'{request.META.get("HTTP_HOST")}')[1]
            return redirect(f'{return_url}')
        elif request.method == "POST":
            try:
                data_object = pod_category_preporat_list.objects.get(id=id)
                newp_form = pod_category_preporat_Form(request.POST)
                if newp_form.is_valid():
                    data_object.name = newp_form.cleaned_data.get('name')
                data_object.save()
            except:
                pass
            return_url = request.META.get('HTTP_REFERER').split(f'{request.META.get("HTTP_HOST")}')[1]
            return redirect(f'{return_url}')
        else:
            return HttpResponse('405 Method Not Allowed', status=405)
    return redirect('/')


def proizvoditel(request):
    arguments = {}
    arguments.update(name_tag=['производителя', 'Производители', 'производителей', 'производителя'])
    arguments.update(form=proizvoditel_Form)
    arguments.update(data_search=proizvoditel_list.objects.all().filter(del_status=1))
    data = []
    for i, item in enumerate(arguments['data_search']):
        data.append({'form': proizvoditel_Form(instance=item), 'id': item.id})
    arguments.update(data_edit=data)
    if request.user.is_authenticated and has_group(request.user, 'Администратор'):
        if request.method == "GET":
            return render(request, 'mainapp/admin/proizvoditel_list.html', {'arguments': arguments})
        elif request.method == "POST":
            newdata_form = proizvoditel_Form(request.POST)
            if newdata_form.is_valid():
                newdata_form.save()
                return_url = request.META.get('HTTP_REFERER').split(f'{request.META.get("HTTP_HOST")}')[1]
                return redirect(f'{return_url}')
            else:
                arguments.update(error="Форма добавления заполнена не корректно!")
                arguments.update(form=newdata_form)
                return render(request, 'mainapp/admin/proizvoditel_list.html', {'arguments': arguments})
        else:
            return HttpResponse('405 Method Not Allowed', status=405)
    return redirect('/')


def proizvoditel_updater(request, id):
    arguments = {}
    if request.user.is_authenticated and has_group(request.user, 'Администратор'):
        if request.method == "GET":
            try:
                data_object = proizvoditel_list.objects.get(id=id)
                data_object.del_status = 0
                data_object.save()
            except:
                pass
            return_url = request.META.get('HTTP_REFERER').split(f'{request.META.get("HTTP_HOST")}')[1]
            return redirect(f'{return_url}')
        elif request.method == "POST":
            try:
                data_object = proizvoditel_list.objects.get(id=id)
                newp_form = proizvoditel_Form(request.POST)
                if newp_form.is_valid():
                    data_object.name = newp_form.cleaned_data.get('name')
                    data_object.zavod_name = newp_form.cleaned_data.get('zavod_name')
                    data_object.country_id = newp_form.cleaned_data.get('country_id')
                data_object.save()
            except:
                pass
            return_url = request.META.get('HTTP_REFERER').split(f'{request.META.get("HTTP_HOST")}')[1]
            return redirect(f'{return_url}')
        else:
            return HttpResponse('405 Method Not Allowed', status=405)
    return redirect('/')


def preporat(request):
    arguments = {}
    arguments.update(name_tag=['препарат', 'Препараты', 'препаратов', 'препарата'])
    if request.user.is_authenticated:
        if has_group(request.user, 'Администратор'):
            try:
                arguments.update(form=preporat_Form)
                arguments.update(data_search=preporat_list.objects.all().filter(del_status=1))
                data = []
                for i, item in enumerate(arguments['data_search']):
                    data.append({'form': preporat_Form(instance=item), 'id': item.id})
                arguments.update(data_edit=data)
            except:
                pass
            if request.method == "GET":
                return render(request, 'mainapp/admin/preporat_list.html', {'arguments': arguments})
            elif request.method == "POST":
                newdata_form = preporat_Form(request.POST)
                if newdata_form.is_valid():
                    newdata_form.save()
                    return_url = request.META.get('HTTP_REFERER').split(f'{request.META.get("HTTP_HOST")}')[1]
                    return redirect(f'{return_url}')
                else:
                    arguments.update(error="Форма добавления заполнена не корректно!")
                    arguments.update(form=newdata_form)
                    return render(request, 'mainapp/admin/preporat_list.html', {'arguments': arguments})
            else:
                return HttpResponse('405 Method Not Allowed', status=405)
        elif has_group(request.user, 'Фармацевт'):
            arguments.update(data_search=preporat_list.objects.all().filter(del_status=1))
            if request.method == "GET":
                return render(request, 'mainapp/farmac/preporat_list.html', {'arguments': arguments})
            elif request.method == "POST":
                query = request.POST.get('query', None)
                if query is not None:
                    arguments.update(data_search=preporat_list.objects.filter(del_status=1, name__contains=query))
                    arguments.update(query_data=query)
                    print(arguments['data_search'])
                return render(request, 'mainapp/farmac/preporat_list.html', {'arguments': arguments})
        else:
            return redirect('/')
    return redirect('/')


def preporat_updater(request, id):
    arguments = {}
    if request.user.is_authenticated and has_group(request.user, 'Администратор'):
        if request.method == "GET":
            try:
                data_object = preporat_list.objects.get(id=id)
                data_object.del_status = 0
                data_object.save()
            except:
                pass
            return_url = request.META.get('HTTP_REFERER').split(f'{request.META.get("HTTP_HOST")}')[1]
            return redirect(f'{return_url}')
        elif request.method == "POST":
            try:
                data_object = preporat_list.objects.get(id=id)
                newp_form = preporat_Form(request.POST)
                if newp_form.is_valid():
                    data_object.name = newp_form.cleaned_data.get('name')
                    data_object.proizvoditel_id = newp_form.cleaned_data.get('proizvoditel_id')
                    data_object.pod_category_preporat_id = newp_form.cleaned_data.get('pod_category_preporat_id')
                    data_object.brend_id = newp_form.cleaned_data.get('brend_id')
                    data_object.price = newp_form.cleaned_data.get('price')
                    data_object.recept = newp_form.cleaned_data.get('recept')
                data_object.save()
            except:
                pass
            return_url = request.META.get('HTTP_REFERER').split(f'{request.META.get("HTTP_HOST")}')[1]
            return redirect(f'{return_url}')
        else:
            return HttpResponse('405 Method Not Allowed', status=405)
    return redirect('/')


def postavki(request):
    arguments = {}
    arguments.update(name_tag=['поставку', 'Поставки', 'поставок', 'поставки'])
    arguments.update(form=postavki_Form)
    arguments.update(data_search=postavki_list.objects.all().filter(del_status=1))
    if request.user.is_authenticated and has_group(request.user, 'Администратор'):
        if request.method == "GET":
            return render(request, 'mainapp/admin/postavki_list.html', {'arguments': arguments})
        elif request.method == "POST":
            newdata_form = postavki_Form(request.POST)
            if newdata_form.is_valid():
                date_postavki = newdata_form.cleaned_data['date_postavki']
                if date_postavki >= datetime.date.today():
                    newdata = newdata_form.save()
                    newdata.date_postavki = date_postavki
                    newdata.save()
                    return_url = request.META.get('HTTP_REFERER').split(f'{request.META.get("HTTP_HOST")}')[1]
                    return redirect(f'{return_url}{newdata.id}/elements/')
                else:
                    arguments.update(error="Дата заполнена не корректно!")
                    arguments.update(form=newdata_form)
                    return render(request, 'mainapp/admin/postavki_list.html', {'arguments': arguments})
            else:
                arguments.update(error="Форма добавления заполнена не корректно!")
                arguments.update(form=newdata_form)
                return render(request, 'mainapp/admin/postavki_list.html', {'arguments': arguments})
        else:
            return HttpResponse('405 Method Not Allowed', status=405)
    return redirect('/')


def postavki_updater(request, id):
    arguments = {}
    if request.user.is_authenticated and has_group(request.user, 'Администратор'):
        if request.method == "GET":
            try:
                data_object = postavki_list.objects.get(id=id)
                data_object.del_status = 0
                data_object.save()
            except:
                pass
            # return_url = request.META.get('HTTP_REFERER').split(f'{request.META.get("HTTP_HOST")}')[1]
            # return redirect(f'{return_url}')
            return redirect(f'/app/postavki/')
        elif request.method == "POST":
            try:
                data_object = postavki_list.objects.get(id=id)
                newp_form = postavki_Form(request.POST)
                if newp_form.is_valid():
                    date_postavki = newp_form.cleaned_data['date_postavki']
                    if date_postavki >= datetime.date.today():
                        data_object.postavchiki_id = newp_form.cleaned_data.get('postavchiki_id')
                        data_object.date_postavki = date_postavki
                    else:
                        data_object.date_postavki = datetime.date.today()
                data_object.save()
            except:
                pass
            return_url = request.META.get('HTTP_REFERER').split(f'{request.META.get("HTTP_HOST")}')[1]
            return redirect(f'{return_url}')
        else:
            return HttpResponse('405 Method Not Allowed', status=405)
    return redirect('/')


def postavki_accept(request, postavka_id, query_type):
    arguments = {}
    if request.user.is_authenticated and has_group(request.user, 'Администратор'):
        if request.method == "GET" and query_type == 'accept':
            try:
                data_object = postavki_list.objects.get(id=postavka_id)
                if data_object.date_postavki >= datetime.date.today():
                    data_object.status_postavki = 1
                    update_postavka_item(postavka_id)
                    postavki_elem_object = postavki_element_list.objects.filter(postavki_id=postavka_id, del_status=1)
                    for i, item in enumerate(postavki_elem_object):
                        preporat_object = preporat_list.objects.get(id=item.preporat_id.id)
                        preporat_object.count += item.count
                        preporat_object.save()
                else:
                    data_object.date_postavki = datetime.date.today()
                data_object.save()
            except:
                pass
            return_url = request.META.get('HTTP_REFERER').split(f'{request.META.get("HTTP_HOST")}')[1]
            return redirect(f'{return_url}')
        else:
            return HttpResponse('405 Method Not Allowed', status=405)
    return redirect('/')


def postavki_elem(request, postavka_id):
    arguments = {}
    arguments.update(name_tag=['товар', 'Товары', 'товаров', 'товара', 'поставку'])
    arguments.update(form=postavki_element_Form)
    try:
        arguments.update(data_search=postavki_element_list.objects.all().filter(del_status=1, postavki_id=postavka_id))
        data = []
        for i, item in enumerate(arguments['data_search']):
            data.append({'form': postavki_element_Form(instance=item), 'id': item.id})
        arguments.update(data_edit=data)

        arguments.update(postavka=postavki_list.objects.get(del_status=1, id=postavka_id))
        arguments.update(form_postavka=postavki_Form(instance=arguments['postavka']))
    except:
        pass

    if request.user.is_authenticated and has_group(request.user, 'Администратор'):
        if request.method == "GET":
            return render(request, 'mainapp/admin/postavki_elem_list.html', {'arguments': arguments})
        elif request.method == "POST":
            newdata_form = postavki_element_Form(request.POST)
            if newdata_form.is_valid():
                newdata_form.save(postavki_id=postavka_id)
                update_postavka_item(postavka_id)
                return_url = request.META.get('HTTP_REFERER').split(f'{request.META.get("HTTP_HOST")}')[1]
                return redirect(f'{return_url}')
            else:
                arguments.update(error="Форма добавления заполнена не корректно!")
                arguments.update(form=newdata_form)
                return render(request, 'mainapp/admin/postavki_elem_list.html', {'arguments': arguments})
        else:
            return HttpResponse('405 Method Not Allowed', status=405)
    return redirect('/')


def postavki_elem_updater(request, postavka_id, id):
    arguments = {}
    if request.user.is_authenticated and has_group(request.user, 'Администратор'):
        if request.method == "GET":
            try:
                data_object = postavki_element_list.objects.get(id=id)
                data_object.del_status = 0
                data_object.save()
                update_postavka_item(postavka_id)
            except:
                pass
            return_url = request.META.get('HTTP_REFERER').split(f'{request.META.get("HTTP_HOST")}')[1]
            return redirect(f'{return_url}')
        elif request.method == "POST":
            try:
                data_object = postavki_element_list.objects.get(id=id)
                newp_form = postavki_element_Form(request.POST)
                if newp_form.is_valid():
                    data_object.preporat_id = newp_form.cleaned_data.get('preporat_id')
                    data_object.postavka_price = newp_form.cleaned_data.get('postavka_price')
                    data_object.count = newp_form.cleaned_data.get('count')
                data_object.save()
                update_postavka_item(postavka_id)
            except:
                pass
            return_url = request.META.get('HTTP_REFERER').split(f'{request.META.get("HTTP_HOST")}')[1]
            return redirect(f'{return_url}')
        else:
            return HttpResponse('405 Method Not Allowed', status=405)
    return redirect('/')


def sell(request):
    arguments = {}
    arguments.update(name_tag=['продажу', 'Продажи', 'продаж', 'продажи'])
    if request.user.is_authenticated:
        if has_group(request.user, 'Администратор'):
            if request.method == "GET":
                try:
                    ispol_status = request.GET['ispol']
                except:
                    ispol_status = None
                if ispol_status != None:
                    arguments.update(
                        data_search=sell_list.objects.filter(del_status=1, status_sell=ispol_status).order_by(
                            "date_time"))
                else:
                    arguments.update(data_search=sell_list.objects.filter(del_status=1).order_by("-date_time"))
                return render(request, 'mainapp/admin/sell_list.html', {'arguments': arguments})
        elif has_group(request.user, 'Фармацевт'):
            arguments.update(
                data_search=sell_list.objects.filter(del_status=1, sell_user_id=request.user.id).order_by(
                    "-date_time"))
            if request.method == "GET":
                return render(request, 'mainapp/farmac/sell_list.html', {'arguments': arguments})
            elif request.method == "POST":
                try:
                    last_tranzak = \
                        sell_list.objects.filter(sell_user_id=request.user, del_status=1).order_by('-date_time')[:1][0]
                    last_tranzak_status = last_tranzak.status_sell
                except:
                    last_tranzak_status = True
                if last_tranzak_status == True:
                    new_sell = sell_list.objects.create(sell_user_id=request.user)
                    new_sell.save()
                    return_url = request.META.get('HTTP_REFERER').split(f'{request.META.get("HTTP_HOST")}')[1]
                    return redirect(f'{return_url}{new_sell.id}/elements/')
                else:
                    arguments.update(error="У вас имеется не исполненая продажа!")
                    return render(request, 'mainapp/farmac/sell_list.html', {'arguments': arguments})
            else:
                return HttpResponse('405 Method Not Allowed', status=405)
        return redirect('/')
    return redirect('/')


def sell_updater(request, id):
    arguments = {}
    if request.user.is_authenticated and has_group(request.user, 'Фармацевт'):
        if request.method == "GET":
            try:
                data_object = sell_list.objects.get(id=id)
                data_object.del_status = 0
                data_object.save()
            except:
                pass
            return redirect(f'/app/sell/')
        else:
            return HttpResponse('405 Method Not Allowed', status=405)
    return redirect('/')


def sell_accept(request, sell_id, query_type):
    arguments = {}
    if request.user.is_authenticated and has_group(request.user, 'Фармацевт'):
        if request.method == "GET" and query_type == 'accept':
            try:
                data_object = sell_list.objects.get(id=sell_id)
                if data_object.total_count > 0:
                    data_object.status_sell = 1
                    data_object.date_time = timezone.now()
                    update_sell_item(sell_id)
                    sell_elem_object = sell_element_list.objects.filter(sell_id=sell_id, del_status=1)
                    for i, item in enumerate(sell_elem_object):
                        preporat_object = preporat_list.objects.get(id=item.preporat_id.id)
                        preporat_object.count -= item.count
                        preporat_object.save()
                    data_object.save()
                else:
                    usr.set_error('Вы не можете провести продажу, если в ней нет препаратов!')
            except:
                pass
            return_url = request.META.get('HTTP_REFERER').split(f'{request.META.get("HTTP_HOST")}')[1]
            return redirect(f'{return_url}')
        else:
            return HttpResponse('405 Method Not Allowed', status=405)
    return redirect('/')


def sell_elem(request, sell_id, **kwargs):
    arguments = {}
    arguments.update(name_tag=['товар', 'Товары', 'товаров', 'товара', 'продажу'])
    if request.user.is_authenticated:
        if has_group(request.user, 'Администратор'):
            try:
                arguments.update(sell=sell_list.objects.get(del_status=1, id=sell_id))
                arguments.update(data_search=sell_element_list.objects.all().filter(del_status=1, sell_id=sell_id))
            except:
                pass
            if request.method == "GET":
                return render(request, 'mainapp/admin/sell_elem_list.html', {'arguments': arguments})
            else:
                return HttpResponse('405 Method Not Allowed', status=405)
        elif has_group(request.user, 'Фармацевт'):
            try:
                arguments.update(form=sell_element_Form)
                arguments.update(sell=sell_list.objects.get(del_status=1, id=sell_id, sell_user_id=request.user))
                arguments.update(data_search=sell_element_list.objects.all().filter(del_status=1, sell_id=sell_id, ))
                data = []
                for i, item in enumerate(arguments['data_search']):
                    data.append({'form': sell_element_Form(instance=item), 'id': item.id})
                arguments.update(data_edit=data)
            except:
                pass
            if request.method == "GET":
                if usr.get_error_status():
                    arguments.update(error=usr.get_error())
                return render(request, 'mainapp/farmac/sell_elem_list.html', {'arguments': arguments})
            elif request.method == "POST":
                newdata_form = sell_element_Form(request.POST)
                if newdata_form.is_valid():
                    preporat_id = newdata_form.cleaned_data.get('preporat_id')
                    preporat_count = newdata_form.cleaned_data.get('count')
                    preporat_object = preporat_list.objects.get(id=preporat_id.id)
                    sell_list_object = sell_list.objects.get(id=sell_id, del_status=1)
                    if (preporat_object.count - sell_list_object.total_count) >= preporat_count:
                        newdata_form.save(sell_id=sell_id, price=preporat_object.price)
                        update_sell_item(sell_id)
                        return_url = request.META.get('HTTP_REFERER').split(f'{request.META.get("HTTP_HOST")}')[1]
                        return redirect(f'{return_url}')
                    else:
                        arguments.update(
                            error=f"Не хватает выбранного препарата на складе, доступно {preporat_object.count - sell_list_object.total_count}!")
                        arguments.update(form=newdata_form)
                        return render(request, 'mainapp/farmac/sell_elem_list.html', {'arguments': arguments})
                else:
                    arguments.update(error="Форма добавления заполнена не корректно!")
                    arguments.update(form=newdata_form)
                    return render(request, 'mainapp/farmac/sell_elem_list.html', {'arguments': arguments})
            else:
                return HttpResponse('405 Method Not Allowed', status=405)
    return redirect('/')


def sell_elem_updater(request, sell_id, id):
    arguments = {}
    if request.user.is_authenticated and has_group(request.user, 'Фармацевт'):
        if request.method == "GET":
            try:
                data_object = sell_element_list.objects.get(id=id)
                data_object.del_status = 0
                data_object.save()
                update_sell_item(sell_id)
            except:
                pass
            return_url = request.META.get('HTTP_REFERER').split(f'{request.META.get("HTTP_HOST")}')[1]
            return redirect(f'{return_url}')
        elif request.method == "POST":
            try:
                data_object = sell_element_list.objects.get(id=id)
                newp_form = sell_element_Form(request.POST)
                if newp_form.is_valid():
                    preporat_id = newp_form.cleaned_data.get('preporat_id')
                    preporat_count = newp_form.cleaned_data.get('count')
                    preporat_object = preporat_list.objects.get(id=preporat_id.id)
                    sell_list_object = sell_list.objects.get(id=sell_id, del_status=1)
                    if (preporat_object.count - sell_list_object.total_count + data_object.count) >= preporat_count:
                        data_object.preporat_id = newp_form.cleaned_data.get('preporat_id')
                        data_object.count = newp_form.cleaned_data.get('count')
                    else:
                        arguments.update(
                            error=f"Не хватает выбранного препарата на складе, доступно {preporat_object.count - sell_list_object.total_count}!")
                        usr.set_error(arguments['error'])
                else:
                    arguments.update(error="Форма добавления заполнена не корректно!")
                    usr.set_error(arguments['error'])
                data_object.save()
                update_sell_item(sell_id)
            except:
                pass
            return_url = request.META.get('HTTP_REFERER').split(f'{request.META.get("HTTP_HOST")}')[1]
            return redirect(f'{return_url}')
        else:
            return HttpResponse('405 Method Not Allowed', status=405)
    return redirect('/')
