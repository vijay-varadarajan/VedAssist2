from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,Transaction,Medicine

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Transaction, )
admin.site.register(Medicine, )

