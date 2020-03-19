from django.db import models
from consumer.models import Consumer
from provider.models import Item

# Create your models here.
class Review(models.Model):
    comment=models.CharField(max_length=250,null=True)
    rating=models.FloatField()
    consumer=models.OneToOneField(Consumer,on_delete=models.CASCADE)
    item=models.ForeignKey(Item,on_delete=models.CASCADE,null=True)