from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage

# Create your views here.
def index(request):
    return render(request, "vedassist/index.html")

def predict(request):
    return render(request, "vedassist/predict.html")

def shop(request):  
    return render(request, "vedassist/shop.html")

def login(request):
    try:
        username = request.GET['username']
        password = request.GET['password']
        # user = authenticate(username=n1, password=n2)
        

    except :
        print("Login failed")
        pass    
    return render(request, "login.html")

def signup(request):
    try:
        name = request.GET['name']
        username = request.GET['username']
        password = request.GET['password']
        confpass = request.GET['confirmpassword']
        if password == confpass:
            str1 = "<h1>"+name+"</h1><br>" +"<h1>"+username+"</h1><br>" +"<h1>"+password+"</h1><br>" +"<h1>"+confpass+"</h1><br>" 
            return HttpResponse(str1)
        else:
            return HttpResponse("Wrong lol")
    except :
        print("Register failed")
        pass    
        
    return render(request, "signup.html")
