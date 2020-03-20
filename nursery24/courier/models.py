from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Courier(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    phone_number=models.CharField(max_length=10,blank=False)
    user_type=models.CharField(max_length=10,null=True)

class Address(models.Model):
    addr=models.TextField(max_length=100,null=True)
    courier=models.ForeignKey(Courier,on_delete=models.CASCADE)