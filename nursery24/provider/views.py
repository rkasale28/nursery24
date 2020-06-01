from django.shortcuts import render,redirect
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
from django.db.models import Sum,Avg,Max,Min
from django.contrib.auth.decorators import login_required


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
        data={}
        data['msg']='Username already exists'
        return render(request,'psignup.html',data)
        
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
                data={}
                data['msg']='User does not exist'
                return render(request,'plogin.html',data)
            else:
                auth.login(request,user)
                return redirect('../provider/home')
        else:
            data={}
            data['msg']='Invalid Credentials'
            return render(request,'plogin.html',data)
    else:
        return render(request,'login')

def logout(request):
    auth.logout(request)
    return redirect ('../provider/login')

@login_required(login_url='../provider/login')
def home(request):
    list=request.user.provider.productinorder_set.all().filter(status='P').order_by('order__date_placed')
    return render(request,'phome.html',{'list':list})

@login_required(login_url='../provider/login')
def additem(request):
    productform=ProductForm()
    priceform=PriceForm()
    return render(request,'padditem.html',{'productform':productform,'priceform':priceform})

@login_required(login_url='../provider/login')
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

@login_required(login_url='../provider/login')
def removeitem(request):
    objects=request.user.provider.price_set.all().order_by('product__name')
    return render(request,'premoveitem.html',{'objects':objects})

@login_required(login_url='../provider/login')
def removeitemsubmit(request):
    if (request.method=='POST'):
        product_id=request.POST['id']
        provider_id=request.POST['proid']
        product=Product.objects.get(pk=product_id)
        provider=Provider.objects.get(pk=provider_id)
        Price.objects.get(provider=provider,product=product).delete()
        if (product.providers.all().count()==0):
            product.delete()
        return redirect('../provider/removeitem')

@login_required(login_url='../provider/login')
def addbranch(request):
    form=AddressForm()
    return render(request,'paddbranch.html',{'form':form})

@login_required(login_url='../provider/login')
def myprofile(request):
    return render(request,'pprofile.html')

@login_required(login_url='../provider/login')
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

@login_required(login_url='../provider/login')
def removebranch(request):
    return render(request,'premovebranch.html')

@login_required(login_url='../provider/login')
def removebranchsubmit(request):
    if request.method=='POST':
        address_id=request.POST['id']
        Address.objects.get(pk=address_id).delete()
        return redirect('../provider/removebranch')

@login_required(login_url='../provider/login')
def edit(request):
    userform=UserForm()
    userform.fields['first_name'].initial=request.user.first_name
    userform.fields['last_name'].initial=request.user.last_name
    userform.fields['email'].initial=request.user.email
    providerform=ProviderForm()
    providerform.fields['phone_number'].initial=Provider.objects.get(user=request.user).phone_number
    providerform.fields['shop_name'].initial=Provider.objects.get(user=request.user).shop_name
    return render(request,'peditprofile.html',{'userform':userform,'providerform':providerform})

@login_required(login_url='../provider/login')
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

@login_required(login_url='../provider/login')
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

@login_required(login_url='../provider/login')
def readytoshipsubmit(request):
    if request.method=='POST':
        id=request.POST['id']
        addr=request.POST['addr']
        product=ProductInOrder.objects.get(pk=id)
        address=Address.objects.filter(provider=request.user.provider).get(addr=addr)      

        product.status='R'
        product.last_tracked_on=datetime.datetime.now()()
      
        product.provider_addr=addr
        product.provider_point=address.point
        
        try:
            dp=DeliveryPersonnel.objects.filter(assigned=False).filter(available=True).annotate(distance=Distance('existing_location_point', address.point)).order_by('distance').first()
            dp.assigned=True
            dp.save()
            
            product.last_tracked_by=dp
            product.save()
            return redirect('../provider/home')
        except:            
            data={}
            data['msg']='No Delivery Personnel is available'
            return render(request,'phome.html',data)

@login_required(login_url='../provider/login')
def ready(request):
    list=request.user.provider.productinorder_set.all().filter(status='R').order_by('order__date_placed')
    return render(request,'pready.html',{'list':list})

@login_required(login_url='../provider/login')
def ship(request):
    if request.method=='POST':
      id=request.POST['id']
      pio=ProductInOrder.objects.get(pk=id)
      pio.status='S'
      pio.last_tracked_on=datetime.datetime.now()()

      pio.save()
      return redirect('../provider/ready')

@login_required(login_url='../provider/login')
def cancelled(request):
    list=request.user.provider.productinorder_set.all().filter(Q(status='I') | Q(status='C')).order_by('-last_tracked_on')
    return render(request,'pcancelled.html',{'list':list})

@login_required(login_url='../provider/login')
def notreturned(request):
    list=request.user.provider.productinorder_set.all().filter(status='N').order_by('last_tracked_on')
    return render(request,'pnotreturned.html',{'list':list})

@login_required(login_url='../provider/login')
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

@login_required(login_url='../provider/login')
def track(request):
    if request.method=='POST':
      id=request.POST['id']
      pio=ProductInOrder.objects.get(pk=id)
      return render(request,'ptrack.html',{'pio':pio})

@login_required(login_url='../provider/login')
def updateprice(request):        
    if request.method=='POST':
      id=request.POST['id']
      proid=request.POST['proid']
      return render(request,'pupdatepriceform.html',{'id':id,'proid':proid})

@login_required(login_url='../provider/login')
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

@login_required(login_url='../provider/login')
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
        
        c['S']=0
        pio=ProductInOrder.objects.filter(product=i,provider=request.user.provider,status='S')
        for j in pio:
            c['S']+=j.quantity
        
        array.append(c)
    return render(request,'psummary.html',{'array':array})

@login_required(login_url='../provider/login')
def analyse(request):
    data={}
    if request.method=='POST':
        start_date=request.POST['from']
        t=request.POST['to']
    else:
        start_date=(datetime.datetime.now()() + datetime.timedelta(-5)).strftime("%Y-%m-%d")
        t=datetime.datetime.now()().strftime("%Y-%m-%d")
    
    end_date = (datetime.datetime.strptime(t, "%Y-%m-%d")+datetime.timedelta(1)).strftime("%Y-%m-%d")

    data['start_date']=start_date
    data['end_date']=t

    name=[]
    c=[]
    d=[]
    n=[]
    s=[]

    obj=request.user.provider.product_set.all().order_by('name')

    for i in obj:
        name.append(i.name)

        pio=i.productinorder_set.filter(last_tracked_on__range=(start_date,end_date),provider=request.user.provider,status='D',product=i)
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

        pio=i.productinorder_set.filter(last_tracked_on__range=(start_date,end_date),product=i,provider=request.user.provider,status='S') 
        temp_s=0
        for j in pio:
            temp_s+=j.quantity               
        s.append(temp_s)
      
    data['name']=json.dumps(name)
    data['c']=json.dumps(c)
    data['d']=json.dumps(d)
    data['n']=json.dumps(n)
    data['s']=json.dumps(s)
    return render(request,'panalyse.html',data)

def convert(list):
    res=[0 if i is None else i for i in list ]
    return (res)

@login_required(login_url='../provider/login')
def danalyse(request):
    data={}
    if request.method=='POST':
        fr=request.POST['from']
        t=request.POST['to']
        name=request.POST['name']
    else:
        fr=(datetime.datetime.now()() + datetime.timedelta(-5)).strftime("%Y-%m-%d")
        t=datetime.datetime.now()().strftime("%Y-%m-%d")
        name=request.user.provider.product_set.all().order_by('name').first().name
    
    to = (datetime.datetime.strptime(t, "%Y-%m-%d")+datetime.timedelta(1)).strftime("%Y-%m-%d")

    data['start_date']=fr
    data['end_date']=t

    start_date=datetime.datetime.strptime(fr, "%Y-%m-%d")
    end_date=datetime.datetime.strptime(t, "%Y-%m-%d")
    d=(end_date-start_date).days

    obj=request.user.provider.product_set.all().order_by('name').exclude(name=name)
    data['product']=obj
    data['selected']=name 
     
    pro=Product.objects.get(name=name)
    
    dates=[]
    highest=[]
    lowest=[]
    mean=[]
    yours=[]

    for i in range(d+1):
        temp=start_date+datetime.timedelta(i)
        dates.append(temp.strftime("%Y-%m-%d"))

        pio=ProductInOrder.objects.filter(last_tracked_on__date=temp.date(),product=pro,status='D').values('provider').order_by('provider')
        pio=pio.annotate(total=Sum('quantity'))
        tot=pio.count()

        prov=pro.providers.all().count()

        pio=pio.aggregate(Max('total'),Min('total'))
        
        highest.append(pio['total__max'])
        if (prov!=tot):
            lowest.append(0)
        else:
            lowest.append(pio['total__min'])
        
        pio=ProductInOrder.objects.filter(last_tracked_on__date=temp.date(),product=pro,status='D').values('last_tracked_on__date').order_by('last_tracked_on__date')
        pio=pio.annotate(total=Sum('quantity'))
        if not pio:
            mean.append(0)
        else:
            temp_y=0
            for j in pio:
                mean.append (j['total']/prov)
       
        pio=ProductInOrder.objects.filter(last_tracked_on__date=temp.date(),status='D',product=pro,provider=request.user.provider)
        if not pio:
            yours.append(0)
        else:
            temp_y=0
            for j in pio:
                temp_y+=j.quantity
            yours.append(temp_y)

    highest=convert(highest)
    lowest=convert(lowest)
    mean=convert(mean)

    data['dates']=json.dumps(dates)
    data['highest']=json.dumps(highest)
    data['lowest']=json.dumps(lowest)
    data['average']=json.dumps(mean)
    data['yours']=json.dumps(yours)
    
    return render(request,'pdanalyse.html',data)
