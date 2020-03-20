from django.shortcuts import render
from django.http import HttpResponse
from django.db import IntegrityError
from django.contrib.auth.models import User,auth
from .models import Consumer

# Create your views here.
def signup(request):
    return render(request,'csignup.html')

def signup_submit(request):
    try:
        if (request.method=='POST'):
            fname=request.POST["fname"]
            lname=request.POST["lname"]
            email=request.POST["mail"]
            uname=request.POST["uname"]
            pwd=request.POST["pwd"]
            phone=request.POST["phone"]
            user=User.objects.create_user(first_name=fname,last_name=lname,email=email,username=uname,password=pwd)    
            consumer=Consumer(user=user,phone_number=phone,user_type='Consumer')
            consumer.save()
            return HttpResponse ("Info added to database<br>"+fname+"<br>"+lname+"<br>"+email+"<br>"+uname+"<br>"+pwd+"<br>"+phone)
    except IntegrityError as e:
        return HttpResponse ('Username already exists')

def login(request):
    return render(request,'clogin.html')

def login_submit(request):
    if request.method=='POST':
        uname=request.POST["uname"]
        pwd=request.POST["pwd"]
        user=auth.authenticate(username=uname,password=pwd)
        if user is not None:
            auth.login(request,user)
            return render(request,'chome.html')
        else:
            return HttpResponse('Invalid Credentials')
    else:
        return render(request,'login')

def logout(request):
    auth.logout(request)
    return render (request,"chome.html")

def myprofile(request):
    return HttpResponse('My Profile')
    
def home(request):
    return render(request,'chome.html')

def plants(request):
    return render(request,'cplants.html')

def seeds(request):
    return render(request,'cseeds.html')
    
def soil(request):
    return render(request,'csoil.html')
    
def decor(request):
    return render(request,'cdecor.html')
    
def accessories(request):
    return render(request,'caccessories.html')

def sample(request):
    return render(request,'sample.html')