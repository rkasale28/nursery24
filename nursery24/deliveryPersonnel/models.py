from django.db import models
from django.contrib.gis.db import models as gismodel
from django.contrib.auth.models import User

# Create your models here.
class DeliveryPersonnel(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    phone_number=models.CharField(max_length=10,blank=False)
    profile_pic=models.ImageField(upload_to='dps/',default='dps/profile.png')
    assigned=models.BooleanField(default=False)
    available=models.BooleanField(default=True)
    existing_location_addr=models.TextField(max_length=100,null=True)
    existing_location_point = gismodel.PointField(null=True)
    
    