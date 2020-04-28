from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Provider(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    phone_number=models.CharField(max_length=10,blank=False)
    shop_name=models.CharField(max_length=100,blank=False,default="ABC")
    profile_pic=models.ImageField(upload_to='dps/',default='dps/profile.png')

class Address(models.Model):
    addr=models.TextField(max_length=100,null=True)
    provider=models.ForeignKey(Provider,on_delete=models.CASCADE)

class Product(models.Model):
    CATEGORY_CHOICES=[
        ('P','Plants'),
        ('S','Seeds'),
        ('F','Soils and Fertilizers'),
        ('D','Decor'),
        ('A','Accessories')
    ]
    image=models.ImageField(upload_to='pics/')
    name=models.CharField(max_length=100,blank=False)
    category=models.CharField(max_length=1,choices=CATEGORY_CHOICES)
    rating=models.FloatField(default=0.0)
    date_added=models.DateTimeField(auto_now_add=True)
    providers=models.ManyToManyField(Provider,through='Price')

class Price(models.Model):
    provider=models.ForeignKey(Provider,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    price=models.IntegerField()
