from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,Transaction,Medicine

class UserAdmin(UserAdmin):
    model = User
    list_display = ['username', 'email', 'is_active', 'is_superuser', 'balance']


# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Transaction, )
admin.site.register(Medicine, )

