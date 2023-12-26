from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.index, name='index'), 
    path("admin", admin.site.urls),   
    path("get/token",views.get_token,name ="token"),
    path("login", views.login_view, name='login'),
    path("register", views.register_view, name='register'),
    path("activate/<uidb64>/<token>/", views.activate, name="activate"),
    path("logout", views.logout_view, name='logout'),
    path("predict", views.predict_view, name='predict'),
    path("shop", views.shop_view, name='shop'),
    path("shop/search", views.search_view, name='search'),
    path("buy/<medicine_name>/", views.buy_view, name='buy'),
    path("history", views.history_view, name='history'),
]
