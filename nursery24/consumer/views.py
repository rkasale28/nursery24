from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.db import IntegrityError
from django.contrib.auth.models import User,auth
from .models import Consumer,Product,Provider,Order,ProductInOrder,Review
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
from django.urls import reverse
from django.http import JsonResponse
from django.core.mail import EmailMessage
from django.conf import settings
from .utils import render_to_pdf
from django.contrib.gis.geos import Point
from django.contrib.gis.geos import *
from django.contrib.gis.db.models.functions import Distance
from django.forms.models import model_to_dict
from django.db.models import Avg
import datetime
import json
from datetime import date,timedelta
from django.utils.crypto import get_random_string
from django.contrib.gis.measure import D
from weasyprint import HTML, CSS
from django.template.loader import get_template
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
import os
import stripe

# Stripe's Secret API Key 🤫
stripe.api_key = 'sk_test_mMdwoJv6bGHI30Jb5FfoIQgV00iZJNQVQI'

# This is Stripe's Publishable Key
publishable_key = 'pk_test_1VWTyC4sr1TtRWpXMhMMWa6U00jagFandz'


# Create your views here.
@login_required(login_url='../consumer/login')
def pdf_generation(request):
            html_template = get_template('templates/home_page.html')
            pdf_file = HTML(string=html_template).write_pdf()
            response = HttpResponse(pdf_file, content_type='application/pdf')
            response['Content-Disposition'] = 'filename="home_page.pdf"'
            return response

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
        data={}
        data['msg']='Username already exists'
        return render(request,'csignup.html',data)
        
def login(request):
    return render(request,'clogin.html')

def login_submit(request):
    if request.method=='POST':
        uname=request.POST["uname"]
        pwd=request.POST["pwd"]
        print( uname,' ', pwd)
        user=auth.authenticate(username=uname,password=pwd)
        print('authenticates')
        if user is not None:
            print('if')
            try:
                consumer=Consumer.objects.get(user=user)
                print('try')
            except ObjectDoesNotExist as d:
                data={}
                data['msg']='User does not exist'
                return render(request,'clogin.html',data)        
            else:
                print('else')
                auth.login(request,user)
                print('login')
                U = cookies.SimpleCookie()
                U['username'] = user
                print('redirecting')
                return redirect('../consumer/home')
        else:
            data={}
            data['msg']='Invalid Credentials'
            return render(request,'clogin.html',data)
    else:
        return render(request,'login')
    
def logout(request):
    auth.logout(request)
    return redirect('../consumer/home')

@login_required(login_url='../consumer/login')
def myprofile(request):
    return render(request,'cprofile.html')

@login_required(login_url='../consumer/login')
def edit(request):
    userform=UserForm()
    userform.fields['first_name'].initial=request.user.first_name
    userform.fields['last_name'].initial=request.user.last_name
    userform.fields['email'].initial=request.user.email
    consumerform=ConsumerForm()
    consumerform.fields['phone_number'].initial=Consumer.objects.get(user=request.user).phone_number
    return render(request,'ceditprofile.html',{'userform':userform,'consumerform':consumerform})

@login_required(login_url='../consumer/login')
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

@login_required(login_url='../consumer/login')
def addresses(request):
    return render(request,'caddress.html')

@login_required(login_url='../consumer/login')
def addaddress(request):
    form=AddressForm()
    return render(request,'caddaddress.html',{'form':form})

@login_required(login_url='../consumer/login')
def addaddresssubmit(request):
    if request.method=='POST':
        consumer_id=request.POST['consumer']
        addr=request.POST['addr']
        consumer=Consumer.objects.get(pk=consumer_id)
        geolocator = Nominatim(user_agent="consumer")
        location = geolocator.geocode(addr)
        address=Consumer_Address(addr=addr,consumer=consumer,point=Point(location.latitude, location.longitude))
        address.save()
        return redirect('../consumer/addresses')

@login_required(login_url='../consumer/login')
def deleteaddresssubmit(request):
    if request.method=='POST':
        address_id=request.POST['id']
        Consumer_Address.objects.get(pk=address_id).delete()
        return redirect('../consumer/addresses') 
    
def home(request):
    data = {}
    newly_added=Product.objects.all().distinct().order_by('-date_added')[:5]
    today = datetime.datetime.now()
    today = today + timedelta(days=1)
    products = []
    prev_date = today - timedelta(days=7)
    expected_delivery = today + timedelta(days=2)
    day_name= ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday','Sunday']
    day = expected_delivery.weekday()
    if day_name[day] == 'Sunday' or day_name[day] == 'Monday' or day_name[day] == 'Tuesday':
        expected_delivery = expected_delivery + timedelta(days=1)
    distinct_products = []
    while len(distinct_products) < 5:
        trending = Order.objects.filter(date_placed__range = (prev_date,today) )
        for obj in trending:
            prod = ProductInOrder.objects.filter(order_id = obj.id)
            for p in prod:
                products.append(p.product_id)
        distinct_products = set(products)
        distinct_count = []
        trending_products = []
        distinct_products = list(distinct_products)
        for i in distinct_products:
            distinct_count.append(products.count(i))
        for x in range(len(distinct_products)-1):   
            for y in range(0,len(distinct_products)-x-1):
                if(distinct_count[y]<distinct_count[y+1]):
                    temp = distinct_count[y]
                    temp2 = distinct_products[y]
                    distinct_count[y] = distinct_count[y+1]
                    distinct_products[y] = distinct_products[y+1]
                    distinct_count[y+1] = temp
                    distinct_products[y+1] = temp2
        prev_date = prev_date - timedelta(days = 7)
    # print ('Distinct Products: ',distinct_products)
    for i in range(5):
        trending_products.append(Product.objects.get(id = distinct_products[i]))
    ratings=Product.objects.all().distinct().order_by('-rating')[:5]
    print(ratings)
    data['newly_added'] = newly_added
    data['trending'] = trending_products
    data['ratings'] = ratings
    return render(request,'chome.html',data)

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
        individual_price=[]
        for i in range(len(products)):
            product = products[i]
            names.append(product['name'])
            try:
                provider = product['providers'][0]
                provnames.append(provider['providerName'])
                qty.append(provider['quantity'])
                prices.append(provider['price'])
                individual_price.append(provider['perPrice'])
                
            except:
                provnames.append("Single")
                qty.append(product['quantity'])
                prices.append(int(product['price']))
                individual_price.append(product['perPrice'])

        data = {}
        data['names'] = names
        data['qty'] = qty
        data['length'] = range(len(names))
        data['provnames'] = provnames
       
        data['prices'] = prices  
        prices = map(lambda x: int(x),prices)
        data['sum']=sum(prices)    
        data['individual_price']=individual_price

        request.session['names'] = names
        request.session['qty'] = qty
        request.session['provider'] = provnames
    return render(request,'corderpage.html',data) 

@login_required(login_url='../consumer/login')
def selectaddress(request):
    return render(request,'cselectaddress.html') 

@login_required(login_url='../consumer/login')
def displayaddaddressformtoconfirmorder(request):
    return render(request,'cdisplayaddaddressformtoconfirmorder.html')

@login_required(login_url='../consumer/login')
def confirmorder(request):
    consumer=request.user.consumer
    address = request.POST['address']
    try:
        present = Consumer_Address.objects.get(addr=address,consumer=consumer)
    except ObjectDoesNotExist as d:
        geolocator = Nominatim(user_agent="consumer")
        location = geolocator.geocode(address)
        a=Consumer_Address(addr=address,consumer=consumer,point=Point(location.latitude, location.longitude))
        a.save()
    
    cookies = request.COOKIES['product']
    products = json.loads(cookies) 
    
    data={}
    data['names']=[]
    data['per_price']=[]
    data['total_price']=[]
    data['qty']=[]
    data['available']=[]
    providers=[]
    
    cust_pt = Consumer_Address.objects.get(addr=address,consumer=consumer).point
         
    for i in products:
        p=Product.objects.get(name=i['name'])
        try:
            pro=Provider.objects.get(shop_name=i['provider'])
            qty=i['quantity']
            perPrice=i['perPrice']
            price=i['price']
        except:
            pro=Provider.objects.get(shop_name=i['providers'][0]['providerName'])
            qty=i['providers'][0]['quantity']
            perPrice=i['providers'][0]['perPrice']
            price=i['providers'][0]['price']
        pro_addr=Provider_Address.objects.filter(provider=pro.id).annotate(distance=Distance('point', cust_pt)).order_by('distance').first()
        dist=(pro_addr.point.distance(cust_pt)*100)
        if (dist<=50):
            data['names'].append(p.name)
            data['qty'].append(qty)
            data['per_price'].append(perPrice)
            data['total_price'].append(int(price))
            data['available'].append(True)
            providers.append(pro.shop_name)
        else:
            data['names'].append(p.name)
            data['qty'].append(None)
            data['per_price'].append(None)
            data['total_price'].append(0)
            data['available'].append(False)
            providers.append(None)
    
    total=sum(data['total_price'])

    if total>1500:
        delivery = 0
    elif total>1000:
        delivery = 0.07*total
    else:
        delivery = 0.15*total
    
    if total>1500:
        int_h = 0
    elif total>1000:
        int_h = 0.03*total
    else:
        int_h = 0.05*total

    data['total'] = total
    data['delivery'] = int(delivery)
    data['int_handling'] = int(int_h)
    data['grand_total'] = total+int(delivery)+int(int_h)
    data['length']=range(len(data['names']))
    request.session['grand_total'] = data['grand_total']
    request.session['available']=data['available']
    request.session['cust_addr']=address
    request.session['provider']=providers
    return render(request,'confirmorder.html',data)

@login_required(login_url='../consumer/login')
def payments(request):
    api = {}
    cookies = request.COOKIES['product']
    products = json.loads(cookies) 
        
    qty = []
    provider = []
    provnames = []
    prices = []
    individual_price=[]

    for i in range(len(products)):
        product = products[i]
            
        try:
            provider = product['providers'][0]
            prices.append(provider['price'])
                
                
        except:
            provnames.append("Single")
                
            prices.append(product['price'])
             

    data = {}
        
       
    data['provnames'] = provnames
    data['prices'] = prices  
    #prices = map(lambda x: int(x),prices)

    data['sum']=request.session['grand_total']
    api['sum'] = data['sum']
    # intent = stripe.PaymentIntent.create(
    # amount= data['sum'] * 100,
    # currency='inr',
    #  metadata={'integration_check': 'accept_a_payment'},
    # )
    # api['intent'] = intent
    # api['client_secret'] = intent.client_secret;
    api['publishable_key'] = publishable_key
    return render(request,'payments.html',api)

@login_required(login_url='../consumer/login')
def charge(request):
    amount = 0
    if request.method == 'POST':
        print('Data:', request.POST)

        amount = int(request.POST['amount'])

        # customer = stripe.Customer.create(
		#     email=request.POST['email'],
		#     name=request.POST['f_name'] + request.POST['l_name'],
		#     source=request.POST['stripeToken']
		#     )

		# charge = stripe.Charge.create(
        #     customer=customer,
		# 	amount=amount*100,
		# 	currency='inr',
		# 	description="Nursery Store Payment"
		# 	)
    
    return redirect(reverse('success', args=[amount]))

@login_required(login_url='../consumer/login')
def successfulorder(request):
    today = datetime.datetime.now()
    current_time = datetime.datetime.now()
    
    expected_delivery = today + timedelta(days=2)
    day_name= ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday','Sunday']
    
    if current_time.hour < 18:
        expected_delivery = today + timedelta(days=1)
        day = expected_delivery.weekday()
        if day_name[day] == 'Sunday' or day_name[day] == 'Monday':
            expected_delivery = expected_delivery + timedelta(days=1)
    else:
        expected_delivery = today + timedelta(days=2)
        day = expected_delivery.weekday()
        if day_name[day] == 'Sunday' or day_name[day] == 'Monday' or day_name[day] == 'Tuesday':
            expected_delivery = expected_delivery + timedelta(days=1)
    
    unique_id = get_random_string(length = 7)
    current_user = request.user
    consumer = Consumer.objects.get(user_id = current_user.id)
    
    grand_total = request.session['grand_total']
    cust_addr = request.session['cust_addr']
    cust_pt=Consumer_Address.objects.get(consumer_id = consumer.id,addr=cust_addr).point
    
    order=Order(total_price = grand_total,
    secondary_id = unique_id,
    date_placed = today,
    consumer = current_user.consumer,
    delivery_addr = cust_addr,
    delivery_point = cust_pt)

    order.save()
    order=Order.objects.get(secondary_id=unique_id)
    
    data = {}
    data['names']= request.session['names']
    data['qty']=request.session['qty']
    data['addr']=cust_addr
    data['username']=request.user.first_name+' '+request.user.last_name
    data['email']=request.user.email
    providers=request.session['provider']
    available=request.session['available']
    names=[]
    quantity=[]
    t_price=[]
    p=[]

    for i in range(len(data['names'])):
        if available[i]:
            prod=Product.objects.get(name=data['names'][i])
            prov=Provider.objects.get(shop_name=providers[i])
            price=Price.objects.get(provider=prov,product=prod).price
            total_price=price*data['qty'][i]
            
            names.append(data['names'][i])
            quantity.append(data['qty'][i])
            p.append(price)
            t_price.append(total_price)
            
            ProductInOrder(product = prod,
            provider = prov,
            order = order,
            quantity = data['qty'][i],
            total_price = total_price,
            expected_delivery_date = expected_delivery,
            last_tracked_on=today).save()
    
    data['length'] = range(len(names))
    data['total_price']=t_price
    data['per_price']=p
    data['names']=names
    data['qty']=quantity
    data['expected_delivery']=expected_delivery
    data['grand_total']=grand_total
    data['unique_id']=unique_id
    html_string = render_to_string('invoice.html', data)
    html = HTML(string=html_string,base_url=request.build_absolute_uri())
    result = html.write_pdf()

    to = [current_user.email]
    #send_mail('Test Mail','Practice for project',settings.EMAIL_HOST_USER,to,fail_silently=True)
    #pdf = render_to_pdf('invoice.html',data)
    email = EmailMessage(
    'Order Confirmation', 'Invoice attatched as pdf', 'settings.EMAIL_HOST_USER',to)
    if result:
        email.attach('invoice2.pdf',result ,'application/pdf')
        email.send()
    
    return render(request,'csuccessfulorder.html',data)

@login_required(login_url='../consumer/login')
def successMsg(request):
    amount = args
    return render(request, 'previousOrders.html',{'amount':amount})

@login_required(login_url='../consumer/login')
def orderlogin(request):
    return render(request,'corderlogin.html')

@login_required(login_url='../consumer/login')
def orderlogin_submit(request):
    if request.method=='POST':
        uname=request.POST["uname"]
        pwd=request.POST["pwd"]
        user=auth.authenticate(username=uname,password=pwd)
        if user is not None:
            try:
                consumer=Consumer.objects.get(user=user)
            except ObjectDoesNotExist as d:
                data={}
                data['msg']='User does not exist'
                return render(request,'clogin.html',data)        
            else:
                auth.login(request,user)
                U = cookies.SimpleCookie()
                U['username'] = user
                
                return redirect('../consumer/cart')
        else:
            data={}
            data['msg']='Invalid Credentials'
            return render(request,'clogin.html',data)        
    else:
        return render(request,'login')

@login_required(login_url='../consumer/login')
def vieworders(request):
    order=Order.objects.filter(consumer=request.user.consumer).order_by('-date_placed')
    data={}
    dict={}
    data['order']=order
    pio=ProductInOrder.objects.filter(order__consumer=request.user.consumer).distinct('product__name')

    for i in pio:
        r=Review.objects.filter(consumer=request.user.consumer,product=i.product)
        if not r:
            dict[i.product.name]=0
        else:
            dict[i.product.name]=r.first().rating
    
    data['rate']=dict
    
    return render(request,'cvieworder.html',data)

@login_required(login_url='../consumer/login')
def track(request):
    if request.method=='POST':
        id=request.POST["id"]
        pio=ProductInOrder.objects.get(pk=id)
        return render(request,'ctrack.html',{'pio':pio})

@login_required(login_url='../consumer/login')
def cancel(request):
    if request.method=='POST':
        id=request.POST["id"]
        pio=ProductInOrder.objects.get(pk=id)
        pio.last_tracked_on=datetime.datetime.now()

        if (pio.status=='R'):
            pio.status='I'
            pio.save()
            #Send Mail to pio.last_tracked_by
        elif (pio.status=='P'):
            pio.status='C'
            pio.save()
        else:
            pio.status='N'
            pio.save()
        return redirect('../consumer/vieworders')

@login_required(login_url='../consumer/login')
def rate(request):
    if request.method=='POST':
        string=request.POST["stars"]
        stars,pro_id=string.split('?')
        product=Product.objects.get(pk=pro_id)
        try:
            review=Review.objects.get(consumer=request.user.consumer,product=product)
            review.rating=stars
            review.save()
        except ObjectDoesNotExist as d:
            Review(rating=stars,
            consumer=request.user.consumer,
            product=product).save()
        
        r=Review.objects.all().values('product').annotate(Avg('rating')).order_by('product')
        for i in r:
            product=Product.objects.get(pk=i['product'])
            product.rating=i['rating__avg']/5*100
            product.save()
        return HttpResponse(stars)