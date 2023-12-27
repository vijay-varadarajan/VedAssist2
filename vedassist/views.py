from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
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
from django.views.decorators.csrf import csrf_exempt
import joblib, pandas as pd
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
import secrets
from .tokens import account_activation_token

from .models import User, Medicine, Transaction

# Create your views here.



def index(request):
    return render(request, "vedassist/index.html", {
        "user": request.user, 
    })
@csrf_exempt
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
            user_token = generate_token_for_user(username)
            return JsonResponse({"token": user_token} , status = 200)
        # Else, return login page again with error message
        else:
            try:
                user = User.objects.get(username=username)
                
                if not user.is_active:
                    return JsonResponse({"message": "Account not activated, check your email for activation link."} , status = 440)
                
                if not check_password(password, user.password):
                    return JsonResponse({"message" : "Password is Incorrect"} , status = 441)
                
            except User.DoesNotExist:
                return JsonResponse({"message" : "User Doesnt Exist"} , status = 442)

  
        
    

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

@csrf_exempt
def register_view(request):
    if request.method == "POST":
        # Get form input values
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirm_password"] 
        print("Confirmed")
        
        if password != confirmation:
            return JsonResponse({"message": "Password mismatch"} , status = 443)
            
        # Attempt to create new user
        try:
             # type: ignore # create_user() returns a User object
            user = User.objects.create_user(username=username, email=email ,password=password, is_active=False)      # type: ignore
            try:
                activateEmail(request, user, email)
                
                user.save() # save user
                
                return JsonResponse({"message" : "Account created successfully! Check your email for activation link."}, status = 200)
            except ValueError:
                user.delete() # delete user
                return JsonResponse({"message" : "Invalid Mail Id."}, status = 445)
        
            
            
        except IntegrityError:
            return JsonResponse({"message" : "User already exist"} , status = 444)
        
            
        
    

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
        return 1
    else:
        return None


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

    
@csrf_exempt
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
        
        # convert numpy 2d array to list
        medicines = medicines.tolist()
        medicines = medicines[0]
        
        # get medicine details from database
        medicines = [medicine.strip() for medicine in medicines]
        print(medicines)
        
        medicine_details = Medicine.objects.filter(medicine_name__in=medicines)
        print(medicine_details)
        
        if len(medicine_details) == 2:
            
            return JsonResponse({
                "medicines" : [
                    
                        {
                            "name": medicine_details[0].medicine_name,
                            "description": medicine_details[0].medicine_description,
                            "price": medicine_details[0].medicine_price,
                            "image": medicine_details[0].medicine_image.url, 
                        }, 
                        {
                            "name": medicine_details[1].medicine_name,
                            "description": medicine_details[1].medicine_description,
                            "price": medicine_details[1].medicine_price,
                            "image": medicine_details[1].medicine_image.url,
                        }
                ]
            }, status=200)
            
        else:
            return JsonResponse({
                "medicines" : [
                    
                        {
                            "name": medicine_details[0].medicine_name,
                            "description": medicine_details[0].medicine_description,
                            "price": medicine_details[0].medicine_price,
                            "image": medicine_details[0].medicine_image.url, 
                        }, 
                        {
                            "name": medicine_details[1].medicine_name,
                            "description": medicine_details[1].medicine_description,
                            "price": medicine_details[1].medicine_price,
                            "image": medicine_details[1].medicine_image.url,
                        },
                        {
                            "name": medicine_details[2].medicine_name,
                            "description": medicine_details[2].medicine_description,
                            "price": medicine_details[2].medicine_price,
                            "image": medicine_details[2].medicine_image.url,
                        }
                ]
            }, status=200)
        
    return render(request, "vedassist/predict.html")

@csrf_exempt
def model_predict(user_input):

    classifier = joblib.load('vedassist/model.pkl')
    
    # sourcery skip: inline-immediately-returned-variable
    user_input = user_input.split(',')
    user_data = pd.DataFrame({ 
            'Cold': [user_input[0]],
            'Eyepain' :[user_input[1]],
            'Fever': [user_input[2]],
            'Headache': [user_input[3]],
            'Stomachache': [user_input[4]],
            'Dizziness': [user_input[5]],
            'Vomiting': [user_input[6]],
            'Chestpain': [user_input[7]],
            'Jointpain': [user_input[8]],
            'Loosemotion': [user_input[9]],
            'Throatinfection':[user_input[10]],
            'Age': [user_input[11]],
            'Gender': [user_input[12]],
            'Weight': [user_input[13]],
    })
    prediction = classifier.predict(user_data)
    return prediction


@csrf_exempt
def shop_view(request):
    
    # retrieve medicine name from medicines table
    items = Medicine.objects.all()
    
    medicines = []
    
    for item in items:
        medicines.append({
                            "name": item.medicine_name,
                            "description": item.medicine_description,
                            "price": item.medicine_price, 
                        })
        
    
    return JsonResponse({
                "medicines" : medicines,
            }, status=200)

@csrf_exempt
def search_view(request):
    searchText = ""
    items = []
    
    if request.method == "POST":
        data = request.POST
        searchText = data.get('searchText')
        searchText = searchText.capitalize()
        print(searchText)
        items = Medicine.objects.filter(medicine_name__icontains = searchText)
        
    print(items) 
    medicines = []   
    if items != []:
        for item in items:
            print(item)
            medicines.append({
                                "name": item.medicine_name,
                                "description": item.medicine_description,
                                "price": item.medicine_price, 
                            })
    else:
        pass        

        
    
    return JsonResponse({
                "medicines" : medicines,
            }, status=200)


import datetime, random

@login_required(login_url='/login')
@csrf_exempt
def buy_view(request, medicine_name):
    
    if request.method == "POST":
        
        item = Medicine.objects.get(medicine_name=medicine_name)
        user = request.user
        transaction_id = f"{datetime.datetime.now()}{item.medicine_name}{item.medicine_price}{random.randint(1000, 9999)}"
        
        door_no = request.POST.get('door_no')
        street = request.POST.get('street')
        city = request.POST.get('city')
        pincode = request.POST.get('pincode')
        
        Transaction.objects.create(
            user=user,
            medicine=item,
            transaction_id=transaction_id,
            transaction_amount=item.medicine_price,
            transaction_status=True,
            door_no=door_no,
            street=street,
            city=city,
            pincode=pincode,
        )
        
        item.medicine_view_count += 1
        item.save()  # Save the changes to the item object
        
        return HttpResponseRedirect(reverse('shop'))
        
    else:
        item = Medicine.objects.get(medicine_name=medicine_name)
        return render(request, "vedassist/buy.html", {
            "item": item,
        })    
 
 
def history_view(request):
    
    transactions = Transaction.objects.filter(user = request.user)
    
    return render(request, "vedassist/history.html", {
        "transactions": transactions,
    })
    
def generate_token_for_user(username):
    user = User.objects.get(username=username)
    token = default_token_generator.make_token(user)
    return token
