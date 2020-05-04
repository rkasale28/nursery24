from django.db import models
from django.contrib.auth.models import User
from django.contrib.gis.db import models as gismodel

# Create your models here.
class Courier(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    phone_number=models.CharField(max_length=10,blank=False)
    service_name=models.CharField(max_length=100,null=True)
    profile_pic=models.ImageField(upload_to='dps/',default='dps/courier.jpg')

class Address(models.Model):
    addr=models.TextField(max_length=100,null=True)
    point = gismodel.PointField(null=True)
    courier=models.ForeignKey(Courier,on_delete=models.CASCADE)