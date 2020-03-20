from django.db import models
from django.contrib.auth.models import User
from courier.models import Courier
from provider.models import Provider,Product

# Create your models here.
class Consumer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    phone_number=models.CharField(max_length=10,blank=False)

class Address(models.Model):
    addr=models.TextField(max_length=100,null=True)
    consumer=models.ForeignKey(Consumer,on_delete=models.CASCADE)

class Order(models.Model):
    ORDER_STATUS_CHOICES=[
        ('D','Delivered'),
        ('S','Shipped'),
        ('P','Placed')
    ]
    status=models.CharField(max_length=1,choices=ORDER_STATUS_CHOICES,default='P')
    total_price=models.IntegerField()
    date_last_tracked=models.DateField()
    date_delivered=models.DateField()
    consumer=models.ForeignKey(Consumer,on_delete=models.CASCADE)
    last_tracked_by=models.OneToOneField(Courier,on_delete=models.CASCADE)

class ProductInOrder(models.Model):
    product=models.OneToOneField(Product,on_delete=models.CASCADE)
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    provider=models.OneToOneField(Provider,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    total_price=models.IntegerField()

class Review(models.Model):
    comment=models.CharField(max_length=250,null=True)
    rating=models.FloatField()
    consumer=models.OneToOneField(Consumer,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE,null=True)