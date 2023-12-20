from django.shortcuts import render
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


def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"] # username is the name of the input field in the login form
        password = request.POST["password"] # password is the name of the input field in the login form
        user = authenticate(request, username=username, password=password) # authenticate() returns a User object if the credentials are valid for a backend. If not, it returns None.
        # If user is authenticated, login and route to index
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        # Else, return login page again with error message
        else:
            return render(request, "vedassist/login.html", {
                "message": "Invalid username and/or password."
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
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"] 

        if password != confirmation:
            return render(request, "vedassist/register.html", {
                "message": "Passwords must match."
            })
            
        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password) # create_user() returns a User object
            user.save() # save user
            
        except IntegrityError:
            return render(request, "vedassist/register.html", {
                "message": "Username already taken."
            })
        
        # Return to login page with message
        return render(request, "vedassist/login.html", {
            "message": "Account created successfully. Please check your email to activate your account." # message to be displayed in login page
        })
    # If user is not authenticated, return register page
    else:
        return render(request, "vedassist/register.html")
    

def predict_view(request):
    return render(request, "vedassist/predict.html")


def shop_view(request):
    return render(request, "vedassist/shop.html")
