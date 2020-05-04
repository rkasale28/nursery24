from django.urls import path
from . import views

urlpatterns=[
    path('home',views.home,name="home"),
    path('signup',views.signup,name="signup"),
    path('signup_submit',views.signup_submit,name="signup_submit"),
    path('login',views.login,name="login"),
    path('login_submit',views.login_submit,name="login_submit"),
    path('logout',views.logout,name="logout"),
    path('myprofile',views.myprofile,name="myprofile"),
    path('edit',views.edit,name="edit"),
    path('editsubmit',views.editsubmit,name="editsubmit"),
    path('addresses',views.addresses,name="addresses"),
    path('addaddress',views.addaddress,name="addaddress"),
    path('addaddresssubmit',views.addaddresssubmit,name="addaddresssubmit"),
    path('removeaddresssubmit',views.removeaddresssubmit,name="removeaddresssubmit"),
    path('adddp',views.adddp,name="adddp"),
    path('adddpsubmit',views.adddpsubmit,name="adddpsubmit"),
    path('viewdp',views.viewdp,name="viewdp"),
    path('updatedp',views.updatedp,name="updatedp"),
    path('updatedpsubmit',views.updatedpsubmit,name="updatedpsubmit"),
]