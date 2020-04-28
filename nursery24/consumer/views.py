from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
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
from .models import Consumer,Product,Address
from django.core.exceptions import ObjectDoesNotExist
from provider.models import Price
from http import cookies
from .forms import AddressForm,UserForm,ConsumerForm
import json

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
    print("Reached here")
    return redirect('../consumer/home')

def myprofile(request):
    return render(request,'cprofile.html')

def edit(request):
    userform=UserForm()
    userform.fields['first_name'].initial=request.user.first_name
    userform.fields['last_name'].initial=request.user.last_name
    userform.fields['email'].initial=request.user.email
    consumerform=ConsumerForm()
    consumerform.fields['phone_number'].initial=Consumer.objects.get(user=request.user).phone_number
    return render(request,'ceditprofile.html',{'userform':userform,'consumerform':consumerform})

def editsubmit(request):
    if request.method=='POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        email=request.POST['email']
        request.user.first_name=first_name
        request.user.last_name=last_name
        request.user.email=email
        request.user.save()
        phone_number=request.POST['phone_number']
        initial_profile_pic=request.user.consumer.profile_pic.url
        initial_profile_pic=initial_profile_pic.replace('/media/', '')
        profile_pic=request.FILES['profile_pic'] if 'profile_pic' in request.FILES else initial_profile_pic
        consumer=Consumer.objects.get(user=request.user)
        consumer.phone_number=phone_number
        consumer.profile_pic=profile_pic
        consumer.save()
        return redirect('../consumer/myprofile')  
    else: 
        return render(request,'cprofile.html')        

def addresses(request):
    return render(request,'caddress.html')

def addaddress(request):
    form=AddressForm()
    return render(request,'caddaddress.html',{'form':form})

def addaddresssubmit(request):
    if request.method=='POST':
        consumer_id=request.POST['consumer']
        addr=request.POST['addr']
        consumer=Consumer.objects.get(pk=consumer_id)
        address=Consumer_Address(addr=addr,consumer=consumer)
        address.save()
        return redirect('../consumer/addresses')

def deleteaddresssubmit(request):
    if request.method=='POST':
        address_id=request.POST['id']
        Consumer_Address.objects.get(pk=address_id).delete()
        return redirect('../consumer/addresses') 
    
def home(request):
    newly_added=Product.objects.all().distinct().order_by('-date_added')[:5]
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
    prods = Product.objects.all().filter(name__icontains=key).order_by('name') 
    return render(request,'csearch.html',{'products':prods})

def cart(request):
    #key = request.GET['cart']
   # U = cookies.SimpleCookie(os.environ["HTTP_COOKIE"])
    return render(request,'cart.html')

def checkout(request): 
    if request.method == "GET":
       
        
        cookies = request.COOKIES['product']
        products = json.loads(cookies) 
        names = []
        qty = []
        provider = []
        provnames = []
        prices = []

        for i in range(len(products)):
            product = products[i]
            names.append(product['name'])
            try:
                provider = product['providers'][0]
                provnames.append(provider['providerName'])
                qty.append(provider['quantity'])
                prices.append(provider['price'])
                
            except:
                provnames.append("Single")
                qty.append(product['quantity'])
                prices.append(product['price'])
        data = {}
        data['names'] = names
        data['qty'] = qty
        data['length'] = range(len(names))
        data['provnames'] = provnames
        data['prices'] = prices      
        
        request.session['names'] = names
        request.session['qty'] = qty
        request.session['provider'] = provnames
    return render(request,'corderpage.html',data) 

def selectaddress(request):
    current_user = request.user
    consumer = Consumer.objects.get(user_id = current_user.id)
    add = Consumer_Address.objects.filter(consumer_id = consumer.id)
    addr = []
    data = {}
    for a in add:
        addr.append(a.addr)
    data['addr'] = addr
    print(data['addr'])
    return render(request,'cselectaddress.html',data) 


def confirmorder(request):
    address = request.POST['address']
    names = request.session['names']
    qty = request.session['qty']
    provnames = request.session['provider']
    data = {}
    data['names'] = names
    data['qty'] = qty
    data['length'] = range(len(names))
    data['provnames'] = provnames
    finalprices = []
    pri = []
    changed = []
    for i in range(len(names)):
        product = Product.objects.get(name = names[i])
        prov = Provider.objects.filter(price__product_id = product.id)
        nom = Nominatim(timeout = None)
        n = []
        available = []
        prices = []
        d = nom.geocode(address,timeout = None)
        ps = []      
        customeraddr = (d.latitude,d.longitude)
        if provnames[i] == 'Single':
                prov1 = Provider.objects.get(price__product_id = product.id)
                addr = Provider_Address.objects.filter(provider_id = prov1.id)
                for a in addr:
                    n = nom.geocode("%s" % a.addr,timeout = None )
                    provideraddr = (n.latitude,n.longitude)
                    dist = (geodesic(provideraddr,customeraddr).km)    
                if(dist<50):
                    available.append(prov1.id)
                    changed.append('No')
        else:
            if provnames[i] == 'default':
                pri = Price.objects.filter(product_id = product.id )
                for pr in pri:
                    ps.append(pr.price)               
                prov1 = Provider.objects.filter(price__product_id = product.id).filter(price__price = min(ps))
                print(prov1)
            else:
                prov1 = Provider.objects.filter(shop_name = provnames[i])
            addr = Provider_Address.objects.filter(provider_id = prov1[0].id)
            for a in addr:
                n = nom.geocode("%s" % a.addr,timeout = None )
                provideraddr = (n.latitude,n.longitude)
                dist = (geodesic(provideraddr,customeraddr).km)    
            if(dist<50):
                available.append(prov1[0].id)  
                changed.append('No')            
            else:
                for p in prov:
                    addr = Provider_Address.objects.filter(provider_id = p.id)
                    for a in addr:
                        n = nom.geocode("%s" % a.addr,timeout = None )
                        provideraddr = (n.latitude,n.longitude)
                        dist = (geodesic(provideraddr,customeraddr).km)    
                        if(dist<50): 
                            available.append(p.id)  
                            changed.append('Yes')
                            break
        if(len(available) != 0):
            for x in available:
                pro = Price.objects.filter(product_id = product.id).filter(provider_id = x)
                for y in pro:
                    prices.append(y.price)
            finalprices.append(min(prices))
        else:
            finalprices.append(0)
            changed.append('Yes')
    data['prices'] = finalprices
    data['finalprices'] = []
    total = 0
    for i in range(len(names)):
        data['finalprices'].append(int(qty[i])*int(finalprices[i]))
        total = total + int(qty[i])*int(finalprices[i])
    data['total'] = total
    data['changed'] = changed
    print(changed)
    return render(request,'confirmorder.html',data)

def orderlogin(request):
    return render(request,'corderlogin.html')
def orderlogin_submit(request):
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
                
                return redirect('../consumer/cart')
        else:
            return HttpResponse('Invalid Credentials')
    else:
        return render(request,'login')