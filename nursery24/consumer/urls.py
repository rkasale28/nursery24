from django.urls import path
from . import views

urlpatterns=[
    path('signup',views.signup,name="signup"),
    path('signup_submit',views.signup_submit,name="signup_submit"),
    path('login',views.login,name="login"),
    path('login_submit',views.login_submit,name="login_submit"),
    path('logout',views.logout,name="logout"),
    path('myprofile',views.myprofile,name="myprofile"),
    path('home',views.home,name="home"),
    path('plants',views.plants,name="plants"),
    path('seeds',views.seeds,name="seeds"),
    path('soilandfertilizers',views.soil,name="soil"),
    path('decor',views.decor,name="decor"),
    path('accessories',views.accessories,name="accessories"),
]