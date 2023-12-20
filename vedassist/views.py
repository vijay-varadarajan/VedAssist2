from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage

from .models import User, Medicine, Transaction

# Create your views here.
def index(request):
    return render(request, "vedassist/index.html")

def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"] # username is the name of the input field in the login form
        password = request.POST["password"] # password is the name of the input field in the login form
        
        print(username, password)

        user = authenticate(request, username=username, password=password) # authenticate() returns a User object if the credentials are valid for a backend. If not, it returns None.
        
        print(user)
        # If user is authenticated, login and route to index
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        # Else, return login page again with error message
        else:
            try:
                user = User.objects.get(username=username)
                if check_password(password, user.password):
                    login(request, user)
                    return HttpResponseRedirect(reverse("index"))
                else:
                    return render(request, "vedassist/login.html", {
                        "message": "Invalid username and/or password."
                    })
            except User.DoesNotExist:
                return render(request, "vedassist/login.html", {
                    "message": "Invalid username and/or password. User Dont Exist."
                })

    # If user is not authenticated, return login page
    else:
        return render(request, "vedassist/login.html")
    

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register_view(request):
    if request.method == "POST":
        # Get form input values
        username = request.POST["username"]
        password = request.POST["password"]
        confirmation = request.POST["confirm_password"] 
        email = request.POST["email"]
        
        if email == "": email = username + "@example.com"
        
        if password != confirmation:
            return render(request, "vedassist/register.html", {
                "message": "Passwords must match."
            })
            
        # Attempt to create new user
        try:
            user = User.objects.create_user(username=username, email=email ,password=password, is_active=True) # type: ignore # create_user() returns a User object
            user.save() # save user
            
        except IntegrityError:
            return render(request, "vedassist/register.html", {
                "message": "Username already taken."
            })
        
        # Return to login page with message
        return render(request, "vedassist/login.html")
    # If user is not authenticated, return register page
    else:
        return render(request, "vedassist/register.html")
    

def predict_view(request):
    return render(request, "vedassist/predict.html")


def shop_view(request):
    return render(request, "vedassist/shop.html")
