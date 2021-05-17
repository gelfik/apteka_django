from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path(r'userlist/profile/([0-9]+)/(editUser|delUser)', views.userprofile_admin_update),
    re_path(r'userlist/profile/([0-9]+)/', views.userprofile_admin),
    path('userlist/', views.userlist_admin),
    path('profile/', views.userprofile_look),

]
