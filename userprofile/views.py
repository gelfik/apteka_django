from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, permission_required
from datetime import datetime, timedelta, time
from django.utils import timezone
from django.template.context_processors import csrf
from django.contrib.auth.models import User, Group
from django.contrib import auth
from .forms import SignUpForm
import random
from apteka_django.settings import PASS_SYMBOL_COUNT


def gen_one_password(lenght):
    if lenght <= 8:
        x = 1
    elif 8 < lenght <= 12:
        x = 2
    else:
        x = 3
    import random, string
    Pass_Symbol = []
    spec_cymbol = []
    result = []
    spec_cymbol.extend(list("!#$%&()*+-<=>?"))
    Pass_Symbol.extend(list(string.ascii_letters + string.digits))
    psw = ''.join([random.choice(Pass_Symbol) for x in range(int(lenght - x))]) + ''.join(
        [random.choice(spec_cymbol) for x in range(int(x))])
    result.extend(list(psw))
    random.shuffle(result)
    return "".join(result)


def transliterate(name):
    slovar = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e',
              'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'i', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n',
              'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h',
              'ц': 'c', 'ч': 'cz', 'ш': 'sh', 'щ': 'scz', 'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e',
              'ю': 'u', 'я': 'ja', 'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'E',
              'Ж': 'ZH', 'З': 'Z', 'И': 'I', 'Й': 'I', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N',
              'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F', 'Х': 'H',
              'Ц': 'C', 'Ч': 'CZ', 'Ш': 'SH', 'Щ': 'SCH', 'Ъ': '', 'Ы': 'y', 'Ь': '', 'Э': 'E',
              'Ю': 'U', 'Я': 'YA', ',': '', '?': '', ' ': '_', '~': '', '!': '', '@': '', '#': '',
              '$': '', '%': '', '^': '', '&': '', '*': '', '(': '', ')': '', '-': '', '=': '', '+': '',
              ':': '', ';': '', '<': '', '>': '', '\'': '', '"': '', '\\': '', '/': '', '№': '',
              '[': '', ']': '', '{': '', '}': '', 'ґ': '', 'ї': '', 'є': '', 'Ґ': 'g', 'Ї': 'i',
              'Є': 'e', '—': ''}
    for key in slovar:
        name = name.replace(key, slovar[key])
    return name


@permission_required('userprofile.look_user')
def userlist_admin(request):
    arguments = {}
    arguments.update(csrf(request))
    arguments.update(form=SignUpForm)
    arguments.update(group_list=Group.objects.all())
    local_group_list = []

    for i, item in enumerate(Group.objects.all()):
        local_group_list_data = {}
        local_group_list_data.update(group_name=item)
        local_group_list_data.update(
            user_list=User.objects.filter(is_active=1).filter(groups__name=item).order_by('last_name').order_by(
                'first_name').order_by(
                'userprofile__patronymic'))
        local_group_list.append(local_group_list_data)
    arguments.update(all_user=local_group_list)

    if request.method == 'GET':
        return render(request, 'userprofile/admin/users_list.html', {'arguments': arguments})
    elif request.method == 'POST':
        newuser_form = SignUpForm(request.POST)
        if newuser_form.is_valid():
            new_password = gen_one_password(PASS_SYMBOL_COUNT)
            new_username = transliterate(
                newuser_form.cleaned_data.get('first_name')[:1] + newuser_form.cleaned_data.get('last_name'))
            user_in_bd = True
            count = 1
            while user_in_bd:
                if count == 1 and not User.objects.filter(username=new_username).exists():
                    user_in_bd = False
                elif not User.objects.filter(username=f'{new_username}{count}').exists():

                    user_in_bd = False
                    new_username = f'{new_username}{count}'
                else:
                    count += 1
            userform = newuser_form.save(username=new_username, password=new_password)
            userform.refresh_from_db()
            userform.userprofile.last_name = newuser_form.cleaned_data.get('last_name')
            userform.userprofile.first_name = newuser_form.cleaned_data.get('first_name')
            userform.userprofile.patronymic = newuser_form.cleaned_data.get('patronymic')
            userform.userprofile.email = newuser_form.cleaned_data.get('email')
            userform.userprofile.birthday = newuser_form.cleaned_data.get('birthday')
            userform.userprofile.phone = newuser_form.cleaned_data.get('phone')
            userform.groups.add(Group.objects.get(name=request.POST.get('group_name', '')))
            userform.set_password(new_password)
            userform.save()

            arguments.update(form=SignUpForm)
            arguments.update(add_user_data={'password': new_password, 'username': new_username})
            return render(request, 'userprofile/admin/users_list.html', {'arguments': arguments})
        else:
            arguments.update(form=newuser_form)
            return render(request, 'userprofile/admin/users_list.html', {'arguments': arguments})
    else:
        return HttpResponse('405 Method Not Allowed', status=405)


@permission_required('userprofile.look_user')
def userprofile_admin(request, profile_id):
    arguments = {}
    arguments.update(group_list=Group.objects.all())
    try:
        arguments.update(user_data=User.objects.get(id=profile_id))
    except:
        arguments.update(user_data=None)
    if request.method == 'GET':
        return render(request, 'userprofile/admin/user.html', {'arguments': arguments})
    else:
        return HttpResponse('405 Method Not Allowed', status=405)


@permission_required('userprofile.look_user')
def userprofile_admin_update(request, profile_id, query_type):
    arguments = {}
    arguments.update(group_list=Group.objects.all())
    if request.method == 'POST' and query_type == 'delUser':
        user_object = User.objects.get(id=profile_id)
        user_object.is_active = 0
        user_object.save()
        return redirect(f'/user/userlist/profile/{profile_id}/')
    elif request.method == 'POST' and query_type == 'editUser':
        err = False
        user_search = False
        args_status = False
        last_name = request.POST.get('last_name', False)
        first_name = request.POST.get('first_name', False)
        patronymic = request.POST.get('patronymic', False)
        username = request.POST.get('username', False)
        email = request.POST.get('email', False)
        birthday = request.POST.get('birthday', False)
        phone = request.POST.get('phone', False)
        user_group = request.POST.get('user_group', False)
        if request.user.is_staff or request.user.is_superuser:
            is_staff = request.POST.get('is_staff', False)
            is_superuser = request.POST.get('is_superuser', False)

        if last_name and first_name and patronymic and username and email and birthday and phone and user_group:
            args_status = True
            if request.user.is_staff or request.user.is_superuser:
                if is_staff != '' and is_superuser != '':
                    args_status = True
                else:
                    args_status = False
        else:
            arguments.update(error='Форма заполнена не корректно!')
        try:
            user_object = User.objects.get(id=profile_id)
            user_search = True
        except:
            arguments.update(error='Пользователь не найден!')
            err = True
        if err or not args_status:
            if user_search:
                arguments.update(user_data=user_object)
            return render(request, 'userprofile/admin/user.html', {'arguments': arguments})
        else:
            user_object = User.objects.get(id=profile_id)
            user_object.last_name = last_name
            user_object.first_name = first_name
            user_object.userprofile.patronymic = patronymic
            user_object.username = username
            user_object.email = email
            user_object.userprofile.phone = phone
            user_object.userprofile.birthday = birthday
            user_object.groups.clear()
            user_object.groups.add(Group.objects.get(name=user_group))
            if request.user.is_staff or request.user.is_superuser:
                user_object.is_staff = is_staff
                user_object.is_superuser = is_superuser
            user_object.save()
            return redirect(f'/user/userlist/profile/{profile_id}')
    else:
        return HttpResponse('405 Method Not Allowed', status=405)


def userprofile_look(request):
    arguments = {}
    arguments.update(group_list=Group.objects.all())
    if request.method == 'GET':
        return render(request, 'userprofile/profile.html', {'arguments': arguments})
    else:
        return HttpResponse('405 Method Not Allowed', status=405)