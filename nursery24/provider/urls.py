from django.urls import path
from . import views

urlpatterns=[
    path('signup',views.signup,name="signup"),
    path('signup_submit',views.signup_submit,name="signup_submit"),
    path('login',views.login,name="login"),
    path('login_submit',views.login_submit,name="login_submit"),
    path('logout',views.logout,name="logout"),
    path('home',views.home,name="home"),
    path('additem',views.additem,name="additem"),
    path('additemsubmit',views.additemsubmit,name="additemsubmit"),
    path('removeitem',views.removeitem,name="removeitem"),
    path('removeitemsubmit',views.removeitemsubmit,name="removeitemsubmit"),
    path('addbranch',views.addbranch,name="addbranch"),
    path('addbranchsubmit',views.addbranchsubmit,name="addbranchsubmit"),
    path('removebranch',views.removebranch,name="removebranch"),
    path('removebranchsubmit',views.removebranchsubmit,name="removebranchsubmit"),
    path('myprofile',views.myprofile,name="myprofile"),
    
]