from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,Transaction,Medicine

class UserAdmin(UserAdmin):
    model = User
    list_display = ['username', 'email', 'is_active', 'is_superuser', 'balance']

class TransactionAdmin(admin.ModelAdmin):
    list_display = ['transaction_id', 'user', 'medicine', 'transaction_date']

class MedicineAdmin(admin.ModelAdmin):
    list_display = ['medicine_name', 'medicine_price', 'medicine_view_count']

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Medicine, MedicineAdmin)

