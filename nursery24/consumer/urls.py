from django.urls import path
from . import views

urlpatterns=[
    path('home',views.home,name="home"),
    path('plants',views.plants,name="plants"),
    path('seeds',views.seeds,name="seeds"),
    path('soilandfertilizers',views.soil,name="soil"),
    path('decor',views.decor,name="decor"),
    path('accessories',views.accessories,name="accessories")
]