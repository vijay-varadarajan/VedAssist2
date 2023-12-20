from django.contrib.auth.models import AbstractUser
from django.db import models

# Register your models here.
class User(AbstractUser):
    username = models.CharField(max_length=64, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=64)
    balance = models.FloatField(default=100.00)

    def __str__(self) -> str:
        return 'User: ' + self.username
    
    
class Medicine(models.Model):
    user =models.ForeignKey(User , on_delete=models.SET_NULL , null=True,blank=True)
    medicine_name = models.CharField(max_length=100)
    medicine_price = models.FloatField(default=10.00)
    medicine_description= models.TextField(default="Default description")
    medicine_image = models.ImageField(upload_to = "medicine")
    medicine_view_count=models.IntegerField(default=1)
    
    def __str__(self) -> str:
        return self.medicine_name
    

class Transaction(models.Model):
    user =models.ForeignKey(User , on_delete=models.SET_NULL , null=True,blank=True)
    medicine = models.ForeignKey(Medicine , on_delete=models.SET_NULL , null=True,blank=True)
    transaction_id = models.CharField(max_length=100)
    transaction_amount = models.FloatField(default=0)
    transaction_status = models.BooleanField(default=False)
    transaction_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.transaction_id