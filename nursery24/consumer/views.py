from django.shortcuts import render

# Create your views here.
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