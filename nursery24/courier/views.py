from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.db import IntegrityError
from django.contrib.auth.models import User,auth
from .models import Courier,Address
from http import cookies
from .forms import UserForm,AddressForm,CourierForm
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
def home(request):
    return render(request,'cohome.html')

def signup(request):
    return render(request,'cosignup.html')

def signup_submit(request):
    try:
        if (request.method=='POST'):
            sname=request.POST["sname"]
            email=request.POST["mail"]
            uname=request.POST["uname"]
            pwd=request.POST["pwd"]
            phone=request.POST["phone"]
            addr=request.POST["address"]
            user=User.objects.create_user(email=email,username=uname,password=pwd)    
            courier=Courier(user=user,phone_number=phone,service_name=sname)
            courier.save()
            address=Address(addr=addr,courier=courier)
            address.save()
            user=auth.authenticate(username=uname,password=pwd)
            auth.login(request,user)
            return redirect('../courier/home')
    except IntegrityError as e:
        return HttpResponse ('Username already exists')

def login(request):
    return render(request,'cologin.html')

def login_submit(request):
    if request.method=='POST':
        uname=request.POST["uname"]
        pwd=request.POST["pwd"]
        user=auth.authenticate(username=uname,password=pwd)
        if user is not None:
            try:
                courier=Courier.objects.get(user=user)
            except ObjectDoesNotExist as d:
                return HttpResponse('User does not exist')
            else:
                auth.login(request,user)
                U = cookies.SimpleCookie()
                U['username'] = user
                
                return redirect('../courier/home')
        else:
            return HttpResponse('Invalid Credentials')
    else:
        return render(request,'cologin.html')

def logout(request):
    auth.logout(request)
    print("Reached here")
    return redirect('../courier/login')

def myprofile(request):
    return render(request,'coprofile.html')

def edit(request):
    userform=UserForm()
    userform.fields['email'].initial=request.user.email
    courierform=CourierForm()
    courierform.fields['phone_number'].initial=Courier.objects.get(user=request.user).phone_number
    courierform.fields['service_name'].initial=Courier.objects.get(user=request.user).service_name
    return render(request,'coeditprofile.html',{'userform':userform,'courierform':courierform})

def editsubmit(request):
    if request.method=='POST':
        service_name=request.POST['service_name']
        email=request.POST['email']
        request.user.email=email
        request.user.save()
        phone_number=request.POST['phone_number']
        initial_profile_pic=request.user.courier.profile_pic.url
        initial_profile_pic=initial_profile_pic.replace('/media/', '')
        profile_pic=request.FILES['profile_pic'] if 'profile_pic' in request.FILES else initial_profile_pic
        courier=Courier.objects.get(user=request.user)
        courier.phone_number=phone_number
        courier.service_name=service_name
        courier.profile_pic = profile_pic
        courier.save()     
        return redirect('../courier/myprofile')  
    else: 
        return render(request,'coprofile.html')

def addresses(request):
    return render(request,'coaddress.html')

def addaddress(request):
    form=AddressForm()
    return render(request,'coaddaddress.html',{'form':form})

def addaddresssubmit(request):
    if request.method=='POST':
        courier_id=request.POST['courier']
        addr=request.POST['addr']
        courier=Courier.objects.get(pk=courier_id)
        address=Address(addr=addr,courier=courier)
        address.save()
        return redirect('../courier/addresses')

def removeaddresssubmit(request):
    if request.method=='POST':
        address_id=request.POST['id']
        Address.objects.get(pk=address_id).delete()
        return redirect('../courier/addresses')