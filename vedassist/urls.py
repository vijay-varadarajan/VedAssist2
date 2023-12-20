from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("login/", views.login, name='login'),
    path("signup/", views.signup, name='register'),
    path("shop/", views.shop, name='shop'),
    path("predict/", views.predict, name='predict'),
    path("admin/", admin.site.urls),    
]
