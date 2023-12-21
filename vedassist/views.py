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
from django.contrib import messages
from django.template.loader import render_to_string

from .tokens import account_activation_token

from .models import User, Medicine, Transaction

from .predictor import model_predict

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
                
                if not user.is_active:
                    messages.error(request, "Account not activated, check your email for activation link.")
                    return HttpResponseRedirect(reverse("login_view"))
                
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
            user = User.objects.create_user(username=username, email=email ,password=password, is_active=False) # type: ignore # create_user() returns a User object
            user.save() # save user
            
        except IntegrityError:
            return render(request, "vedassist/register.html", {
                "message": "Username already taken."
            })
        
        activateEmail(request, user, email)
        
        # Return to login page with message
        messages.success(request, "Account created successfully! Check your email for activation link.")
        return HttpResponseRedirect(reverse("login"))

    # If user is not authenticated, return register page
    else:
        return render(request, "vedassist/register.html")
    

def activateEmail(request, user, to_email):
    mail_subject = 'Activate your account.'
    message = render_to_string('vedassist/activate_email.html', {
        'user': user.username, 
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http',
    })

    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        print("Email sent")
    else:
        print("Error sending Email")


def activate(request, uidb64, token):
    try:
        user = User.objects.get(pk=force_str(urlsafe_base64_decode(uidb64)))
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, "Account activated successfully!")
        return HttpResponseRedirect(reverse("login"))
    
    messages.error(request, "Activation link expired!")
    return HttpResponseRedirect(reverse("login"))

    

def predict_view(request):
    if request.method == "POST":
        
        user_input = [
        1 if request.POST.get('cold') == 'on' else 0 ,
        1 if request.POST.get('eyepain') == 'on' else 0,
        1 if request.POST.get('fever') == 'on' else 0,
        1 if request.POST.get('headache') == 'on' else 0,
        1 if request.POST.get('stomachache') == 'on' else 0,
        1 if request.POST.get('dizziness') == 'on' else 0,
        1 if request.POST.get('vomiting') == 'on' else 0,
        1 if request.POST.get('chestpain') == 'on' else 0,
        1 if request.POST.get('jointpain') == 'on' else 0,
        1 if request.POST.get('loosemotion') == 'on' else 0,
        1 if request.POST.get('throatinfection') == 'on' else 0,
        int(request.POST.get('age')),
        int(request.POST.get('gender')),
        int(request.POST.get('weight'))
    ]
    
        medicines = model_predict(str(user_input).lstrip('[').rstrip(']'))
        print(medicines)
        
        return render(request, "vedassist/predict.html", {
            "result": medicines
        })
        
    return render(request, "vedassist/predict.html")


def shop_view(request):
    return render(request, "vedassist/shop.html")
