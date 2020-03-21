from django.shortcuts import render
from django.http import HttpResponse
from django.db import IntegrityError
from django.contrib.auth.models import User,auth
from .models import Address,Provider,Product
from .forms import AddressForm,ProductForm
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
def signup(request):
    return render(request,'psignup.html')

def signup_submit(request):
    try:
        if (request.method=='POST'):
            fname=request.POST["fname"]
            lname=request.POST["lname"]
            email=request.POST["mail"]
            uname=request.POST["uname"]
            pwd=request.POST["pwd"]
            phone=request.POST["phone"]
            addr=request.POST["address"]
            shop=request.POST["shop_name"]
            user=User.objects.create_user(first_name=fname,last_name=lname,email=email,username=uname,password=pwd)    
            provider=Provider(user=user,phone_number=phone,shop_name=shop)
            provider.save()
            address=Address(addr=addr,provider=provider)
            address.save()
            user=auth.authenticate(username=uname,password=pwd)
            auth.login(request,user)
            return render(request,'phome.html')
    except IntegrityError as e:
        return HttpResponse ('Username already exists')

def login(request):
    return render(request,'plogin.html')

def login_submit(request):
    if request.method=='POST':
        uname=request.POST["uname"]
        pwd=request.POST["pwd"]
        user=auth.authenticate(username=uname,password=pwd)
        if user is not None:
            try:
                provider=Provider.objects.get(user=user)
            except ObjectDoesNotExist as d:
                return HttpResponse('User does not exist')
            else:
                auth.login(request,user)
                return render(request,'phome.html')
        else:
            return HttpResponse('Invalid Credentials')
    else:
        return render(request,'login')

def logout(request):
    auth.logout(request)
    return render (request,"plogin.html")

def home(request):
    return render(request,'phome.html')

def additem(request):
    form=ProductForm()
    return render(request,'padditem.html',{'form':form})

def additemsubmit(request):
    if request.method=='POST':
        provider_id=request.POST['provider']
        name=request.POST['name']
        image=request.FILES['image']
        category=request.POST['category']
        price=request.POST['price']
            
        provider=Provider.objects.get(pk=provider_id)
        try:
            check_product=Product.objects.get(name=name,price=price)
        except ObjectDoesNotExist as d:
            product=Product(image=image,name=name,price=price,category=category)
            product.save()
            product.providers.add(provider)
        else:
            check_product.providers.add(provider)
        return render(request,'phome.html')

def removeitem(request):
    return render(request,'premoveitem.html')

def removeitemsubmit(request):
    if (request.method=='POST'):
        product_id=request.POST['id']
        provider_id=request.POST['proid']
        product=Product.objects.get(pk=product_id)
        provider=Provider.objects.get(pk=provider_id)
        provider.product_set.remove(product)
        return render(request,'premoveitem.html')

def addbranch(request):
    form=AddressForm()
    return render(request,'paddbranch.html',{'form':form})

def myprofile(request):
    return render(request,'pprofile.html')

def addbranchsubmit(request):
    if request.method=='POST':
        provider_id=request.POST['provider']
        addr=request.POST['addr']
        provider=Provider.objects.get(pk=provider_id)
        address=Address(addr=addr,provider=provider)
        address.save()
        return render(request,'phome.html')

def removebranch(request):
    return render(request,'premovebranch.html')

def removebranchsubmit(request):
    if request.method=='POST':
        address_id=request.POST['id']
        Address.objects.get(pk=address_id).delete()
        return render(request,'phome.html') 