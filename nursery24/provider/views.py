from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.db import IntegrityError
from django.contrib.auth.models import User,auth
from .models import Address,Provider,Product,Price
from .forms import AddressForm,ProductForm,PriceForm,UserForm,ProviderForm
from django.core.exceptions import ObjectDoesNotExist
from geopy.geocoders import Nominatim
from django.contrib.gis.geos import Point
from consumer.models import ProductInOrder
from datetime import date
from deliveryPersonnel.models import DeliveryPersonnel
from django.contrib.gis.db.models.functions import Distance
from django.db.models import Q
import datetime
import json

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

            geolocator = Nominatim(user_agent="provider")
            location = geolocator.geocode(addr)
            address=Address(addr=addr,provider=provider,point=Point(location.latitude, location.longitude))
            address.save()

            user=auth.authenticate(username=uname,password=pwd)
            auth.login(request,user)
            return redirect('../provider/home')
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
                return redirect('../provider/home')
        else:
            return HttpResponse('Invalid Credentials')
    else:
        return render(request,'login')

def logout(request):
    auth.logout(request)
    return redirect ('../provider/login')

def home(request):
    list=request.user.provider.productinorder_set.all().filter(status='P').order_by('order__date_placed')
    return render(request,'phome.html',{'list':list})

def additem(request):
    productform=ProductForm()
    priceform=PriceForm()
    return render(request,'padditem.html',{'productform':productform,'priceform':priceform})

def additemsubmit(request):
    if request.method=='POST':
        provider_id=request.POST['provider']
        name=request.POST['name']
        image=request.FILES['image']
        category=request.POST['category']
        price=request.POST['price']
        provider=Provider.objects.get(pk=provider_id)
        try:
            check_product=Product.objects.get(name=name)
        except ObjectDoesNotExist as d:
            product=Product(image=image,name=name,category=category)
            product.save()
            product.providers.add(provider,through_defaults={'price':price})
        else:
            check_product.providers.add(provider,through_defaults={'price':price})
        return redirect('../provider/removeitem')

def removeitem(request):
    return render(request,'premoveitem.html')

def removeitemsubmit(request):
    if (request.method=='POST'):
        product_id=request.POST['id']
        provider_id=request.POST['proid']
        product=Product.objects.get(pk=product_id)
        provider=Provider.objects.get(pk=provider_id)
        provider.product_set.remove(product)
        return redirect('../provider/removeitem')

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
        geolocator = Nominatim(user_agent="provider")
        location = geolocator.geocode(addr)
        address=Address(addr=addr,provider=provider,point=Point(location.latitude, location.longitude))
        address.save()
        return redirect('../provider/removebranch')

def removebranch(request):
    return render(request,'premovebranch.html')

def removebranchsubmit(request):
    if request.method=='POST':
        address_id=request.POST['id']
        Address.objects.get(pk=address_id).delete()
        return redirect('../provider/removebranch')

def edit(request):
    userform=UserForm()
    userform.fields['first_name'].initial=request.user.first_name
    userform.fields['last_name'].initial=request.user.last_name
    userform.fields['email'].initial=request.user.email
    providerform=ProviderForm()
    providerform.fields['phone_number'].initial=Provider.objects.get(user=request.user).phone_number
    providerform.fields['shop_name'].initial=Provider.objects.get(user=request.user).shop_name
    return render(request,'peditprofile.html',{'userform':userform,'providerform':providerform})

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
        shop_name=request.POST['shop_name']
        initial_profile_pic=request.user.provider.profile_pic.url
        initial_profile_pic=initial_profile_pic.replace('/media/', '')
        profile_pic=request.FILES['profile_pic'] if 'profile_pic' in request.FILES else initial_profile_pic
        provider=Provider.objects.get(user=request.user)
        provider.phone_number=phone_number
        provider.profile_pic=profile_pic
        provider.shop_name=shop_name
        provider.save()
        return redirect('../provider/myprofile')  
    else: 
        return render(request,'pprofile.html')  

def readytoship(request):
    address=[]
    if request.method=='POST':
        id=request.POST['id']
        pio=ProductInOrder.objects.get(id=id)
        cust_pt=pio.order.delivery_point
        addr=Address.objects.filter(provider=request.user.provider).annotate(distance=Distance('point', cust_pt)).order_by('distance')
        for i in addr:
            dist=(i.point.distance(cust_pt)*100)
            if (dist<=50):
                address.append(i.addr)
            else:
                break
        return render(request,'pselectaddress.html',{'address':address,'productinorderid':id})

def readytoshipsubmit(request):
    if request.method=='POST':
        id=request.POST['id']
        addr=request.POST['addr']
        product=ProductInOrder.objects.get(pk=id)
        address=Address.objects.filter(provider=request.user.provider).get(addr=addr)      

        product.status='R'
        product.last_tracked_on=datetime.datetime.now()
      
        product.provider_addr=addr
        product.provider_point=address.point
        
        dp=DeliveryPersonnel.objects.filter(assigned=False).filter(available=True).annotate(distance=Distance('existing_location_point', address.point)).order_by('distance').first()
        dp.assigned=True
        dp.save()
        
        product.last_tracked_by=dp
        product.save()
        return redirect('../provider/home')

def ready(request):
    list=request.user.provider.productinorder_set.all().filter(status='R').order_by('order__date_placed')
    return render(request,'pready.html',{'list':list})

def ship(request):
    if request.method=='POST':
      id=request.POST['id']
      pio=ProductInOrder.objects.get(pk=id)
      pio.status='S'
      pio.last_tracked_on=datetime.datetime.now()

      pio.save()
      return redirect('../provider/ready')

def cancelled(request):
    list=request.user.provider.productinorder_set.all().filter(Q(status='I') | Q(status='C')).order_by('-last_tracked_on')
    return render(request,'pcancelled.html',{'list':list})

def notreturned(request):
    list=request.user.provider.productinorder_set.all().filter(status='N').order_by('last_tracked_on')
    return render(request,'pnotreturned.html',{'list':list})

def returned(request):
    if request.method=='POST':
      id=request.POST['id']
      pio=ProductInOrder.objects.get(pk=id)
      pio.status='C'
      pio.save()
      dp=pio.last_tracked_by
      dp.assigned=False
      dp.save()
      return redirect('../provider/cancelled')

def track(request):
    if request.method=='POST':
      id=request.POST['id']
      pio=ProductInOrder.objects.get(pk=id)
      return render(request,'ptrack.html',{'pio':pio})

def track(request):
    if request.method=='POST':
      id=request.POST['id']
      pio=ProductInOrder.objects.get(pk=id)
      return render(request,'ptrack.html',{'pio':pio})

def updateprice(request):        
    if request.method=='POST':
      id=request.POST['id']
      proid=request.POST['proid']
      return render(request,'pupdatepriceform.html',{'id':id,'proid':proid})


def updatepricesubmit(request):        
    if request.method=='POST':
      id=request.POST['id']
      proid=request.POST['proid']
      price=request.POST['price']
      provider=Provider.objects.get(pk=proid)
      product=Product.objects.get(pk=id)  
      p=Price.objects.get(provider=provider,product=product)     
      p.price=price
      p.save()
      return redirect('../provider/removeitem')

def viewsummary(request):
    array=[]
    obj=request.user.provider.product_set.all()
    for i in obj:
        c={}
        c['name']=i.name
        
        pio=ProductInOrder.objects.filter(product=i,provider=request.user.provider,status='D')
        c['D']=0
        for j in pio:
            c['D']+=j.quantity
        
        c['C']=0
        pio=ProductInOrder.objects.filter(product=i,provider=request.user.provider,status='C')
        for j in pio:
            c['C']+=j.quantity

        pio=ProductInOrder.objects.filter(product=i,provider=request.user.provider,status='I')
        for j in pio:
            c['C']+=j.quantity
        
        c['N']=0
        pio=ProductInOrder.objects.filter(product=i,provider=request.user.provider,status='N')
        for j in pio:
            c['N']+=j.quantity
        
        array.append(c)
    return render(request,'psummary.html',{'array':array})

def analyse(request):
    data={}
    if request.method=='POST':
        start_date=request.POST['from']
        t=request.POST['to']
    else:
        start_date=(datetime.datetime.now() + datetime.timedelta(-5)).strftime("%Y-%m-%d")
        t=datetime.datetime.now().strftime("%Y-%m-%d")
    
    end_date = (datetime.datetime.strptime(t, "%Y-%m-%d")+datetime.timedelta(1)).strftime("%Y-%m-%d")

    data['start_date']=start_date
    data['end_date']=t

    name=[]
    c=[]
    d=[]
    n=[]

    obj=request.user.provider.product_set.all().order_by('name')

    for i in obj:
        name.append(i.name)

        pio=i.productinorder_set.filter(last_tracked_on__range=(start_date,end_date),product=i,provider=request.user.provider,status='D') 
        temp_d=0
        for j in pio:
            temp_d+=j.quantity               
        d.append(temp_d)

        pio=i.productinorder_set.filter(last_tracked_on__range=(start_date,end_date),product=i,provider=request.user.provider, status='C') 
        temp_c=0
        for j in pio:
            temp_c+=j.quantity               
        
        pio=i.productinorder_set.filter(last_tracked_on__range=(start_date,end_date),product=i,provider=request.user.provider, status='I') 
        for j in pio:
            temp_c+=j.quantity               
        c.append(temp_c)

        pio=i.productinorder_set.filter(last_tracked_on__range=(start_date,end_date),product=i,provider=request.user.provider,status='N') 
        temp_n=0
        for j in pio:
            temp_n+=j.quantity               
        n.append(temp_n)
      
    data['name']=json.dumps(name)
    data['c']=json.dumps(c)
    data['d']=json.dumps(d)
    data['n']=json.dumps(n)
    return render(request,'panalyse.html',data)
