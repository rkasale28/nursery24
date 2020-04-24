from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.db import IntegrityError
from django.contrib.auth.models import User,auth
from .models import Consumer,Product,Provider
from .models import Address as Consumer_Address
from provider.models import Address as Provider_Address
from django.core.exceptions import ObjectDoesNotExist
from provider.models import Price
from http import cookies
from django.views.decorators.csrf import csrf_exempt, csrf_protect
import geopy
from geopy.geocoders import Nominatim
from geopy.distance import geodesic 
from geopy.exc import GeocoderTimedOut

import os
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
            consumer=Consumer(user=user,phone_number=phone)
            consumer.save()
            user=auth.authenticate(username=uname,password=pwd)
            auth.login(request,user)
            return redirect('../consumer/home')
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
            try:
                consumer=Consumer.objects.get(user=user)
            except ObjectDoesNotExist as d:
                return HttpResponse('User does not exist')
            else:
                auth.login(request,user)
                U = cookies.SimpleCookie()
                U['username'] = user
                
                return redirect('../consumer/home')
        else:
            return HttpResponse('Invalid Credentials')
    else:
        return render(request,'login')

def logout(request):
    auth.logout(request)
    
    return redirect('../consumer/home')

def myprofile(request):
    return render(request,'consumer/cprofile.html')
    
def home(request):
    newly_added=Product.objects.all().order_by('-date_added')[:5]
    return render(request,'chome.html',{'newly_added':newly_added})

def plants(request):
    unique_price=Price.objects.all().filter(product__category='P').order_by('product__name','price').distinct('product__name')
    return render(request,'cplants.html',{'unique_price':unique_price})

def seeds(request):
    unique_price=Price.objects.all().filter(product__category='S').order_by('product__name','price').distinct('product__name')
    return render(request,'cseeds.html',{'unique_price':unique_price})
    
def soil(request):
    unique_price=Price.objects.all().filter(product__category='F').order_by('product__name','price').distinct('product__name')
    return render(request,'csoil.html',{'unique_price':unique_price})
    
def decor(request):
    unique_price=Price.objects.all().filter(product__category='D').order_by('product__name','price').distinct('product__name')
    return render(request,'cdecor.html',{'unique_price':unique_price})
    
def accessories(request):
    unique_price=Price.objects.all().filter(product__category='A').order_by('product__name','price').distinct('product__name')
    return render(request,'caccessories.html',{'unique_price':unique_price})

def compareprices(request):
    if (request.method=='GET'):
        productid=request.GET['id']
        product=Product.objects.get(pk=productid)
        prices=product.price_set.all().order_by('price')
        return render(request,'compareprice.html',{'prices':prices})

def search(request):
    key = request.GET['search']
    prods = Product.objects.all().filter(name__icontains=key) 
    return render(request,'csearch.html',{'products':prods})

def cart(request):
    #key = request.GET['cart']
   # U = cookies.SimpleCookie(os.environ["HTTP_COOKIE"])
    return render(request,'cart.html')

def checkout(request): 
    if request.method == "GET":
        names = request.GET['names'].split(",")
        qty = request.GET['qty'].split(",")
        data = {}
        data['names'] = names
        data['qty'] = qty
        data['length'] = range(len(names))
        current_user = request.user
        consumer = Consumer.objects.get(user_id = current_user.id)
        add = Consumer_Address.objects.filter(consumer_id = consumer.id)
        addr = []
        for a in add:
            addr.append(a.addr)
        data['addr'] = addr
        request.session['names'] = names
        request.session['qty'] = qty
    return render(request,'corderpage.html',data) 

def confirmorder(request):
    address = request.POST['address']
    names = request.session['names']
    qty = request.session['qty']
    length = len(names)
    data = {}
    data['names'] = names
    data['qty'] = qty
    data['length'] = range(len(names))
    finalprices = []
    for i in range(len(names)):
        product = Product.objects.get(name__icontains = names[i])
        prov = Provider.objects.filter(price__product_id = product.id)
        nom = Nominatim(timeout = None)
        n = []
        available = []
        prices = []
        d = nom.geocode(address,timeout = None)
        customeraddr = (d.latitude,d.longitude)
        for p in prov:
            addr = Provider_Address.objects.filter(provider_id = p.id)
            for a in addr:
                n = nom.geocode("%s" % a.addr,timeout = None )
                provideraddr = (n.latitude,n.longitude)
                dist = (geodesic(provideraddr,customeraddr).km)    
                if(dist<100):
                    available.append(p.id)  
                    break
        if(len(available) != 0):
            for x in available:
                pro = Price.objects.filter(product_id = product.id).filter(provider_id = x)
                for y in pro:
                    prices.append(y.price)
                    finalprices.append(min(prices))
    data['finalprices'] = finalprices
    return render(request,'confirmorder.html',data)