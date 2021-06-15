"""MIPS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, re_path, include

from . import views

urlpatterns = [
    path('', views.app),
    path('auth/login/', views.login),
    path('auth/logout/', views.logout),

    re_path(r'category/([0-9]+)/podcategory/([0-9]+)/', views.podcategory_updater),
    re_path('category/([0-9]+)/podcategory/', views.podcategory),
    re_path(r'category/([0-9]+)/', views.category_updater),
    path('category/', views.category),
    # re_path(r'podcategory/([0-9]+)/', views.podcategory_updater),

    re_path(r'postavchiki/([0-9]+)/', views.postavchiki_updater),
    path('postavchiki/', views.postavchiki),
    re_path(r'brends/([0-9]+)/', views.brends_updater),
    path('brends/', views.brends),
    re_path(r'proizvoditel/([0-9]+)/', views.proizvoditel_updater),
    path('proizvoditel/', views.proizvoditel),
    re_path(r'preporat/([0-9]+)/', views.preporat_updater),
    path('preporat/', views.preporat),

    re_path(r'postavki/([0-9]+)/elements/([0-9]+)/', views.postavki_elem_updater),
    re_path(r'postavki/([0-9]+)/elements/', views.postavki_elem),
    re_path(r'postavki/([0-9]+)/(accept)', views.postavki_accept),
    re_path(r'postavki/([0-9]+)/', views.postavki_updater),
    path('postavki/', views.postavki),

    re_path(r'sell/([0-9]+)/elements/([0-9]+)/', views.sell_elem_updater),
    re_path(r'sell/([0-9]+)/elements/', views.sell_elem),
    re_path(r'sell/([0-9]+)/(accept)', views.sell_accept),
    re_path(r'sell/([0-9]+)/', views.sell_updater),
    path('sell/', views.sell),

    path('pdf/', views.pdf_get),
    # re_path(r'^pdf/$', MyPDFView.as_view(), name='book-detail'),
    # re_path(r'^pdf/$', PDFTemplateView.as_view(template_name='/mainapp/admin/preporat_list.html',
    #                                         filename='my_pdf.pdf'), name='pdf'),
]
