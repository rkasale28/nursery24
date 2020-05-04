from django.urls import path
from . import views

urlpatterns=[
    path('home',views.home,name="home"),
    path('login',views.login,name="login"),
    path('login_submit',views.login_submit,name="login_submit"),
    path('logout',views.logout,name="logout"),
    path('myprofile',views.myprofile,name="myprofile"),
    path('changePassword',views.changepassword,name="changepassword"),
    path('changePasswordsubmit',views.changepasswordsubmit,name="changepassword"),
    path('toggle',views.toggle,name="toggle"),
    path('updatecurrentlocation',views.updatecurrentlocation,name="updatecurrentlocation"),
    path('assigned',views.assigned,name="assigned")
    # path('editsubmit',views.editsubmit,name="editsubmit"),
]