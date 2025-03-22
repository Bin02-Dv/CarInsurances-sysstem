from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import InsurancePolicy, Payment, Claim, Vehicle
from django.contrib import auth
from django.contrib.auth.decorators import login_required

# Create your views here.

def logout(request):
    auth.logout(request)
    return redirect("/login/")

def landing(request):
    return render(request, 'landing-page.html')

def register(request):
    if request.method == 'POST':
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password = request.POST.get("password")
        cpassword = request.POST.get("confirm_password")
        
        username = email[:-10]
        
        if cpassword != password:
            return JsonResponse({"success": False, "message": "Password and confirm password missed match!!"})
        
        if User.objects.filter(email=email).exists():
            return JsonResponse({"success": False, "message": "User with this email already exists!!"})
        
        new_user = User.objects.create_user(first_name=full_name, email=email, last_name=phone, username=username, password=password)
        new_user.save()
        return JsonResponse({"success": True, "message": "Registeration Completed Successfully..."})
        
    return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        user = User.objects.filter(email=email).first()  # Safe query
        
        if user:
            auth_user = auth.authenticate(request, username=user.username, password=password)
            
            if auth_user is not None:
                auth.login(request, auth_user)  # Corrected to use `auth_user`
                return JsonResponse({"success": True, "message": "Login Successfully..."})
            else:
                return JsonResponse({"success": False, "message": "Invalid Credentials!!!"})
        else:
            return JsonResponse({"success": False, "message": "Sorry we couldn't find a user with the specified Email!!"})
    
    return render(request, 'login.html')

@login_required(login_url='/login')
def dash(request):
    current_user = request.user
    
    context = {
        "user": current_user
    }
    return render(request, 'dash.html', context)

def add_policy(request):
    if request.method == 'POST':
        policy_name = request.POST.get("policy_name")
        coverage_type = request.POST.get("coverage_type")
        premium_amount = request.POST.get("premium_amount")
        description = request.POST.get("description")
        duration = request.POST.get("duration")
        
        new_insurancePolicy = InsurancePolicy.objects.create(
            policy_name=policy_name, policy_type=coverage_type, coverage_details=description, premium_amount=premium_amount, duration_months=duration
        )
        new_insurancePolicy.save()
        return JsonResponse({"success": True, "message": "Insurance Policy Added Successfully..."})
    return render(request, 'add-policy.html')

def policy_management(request):
    current_user = request.user
    polices =  InsurancePolicy.objects.all()
    
    context = {
        'polices': polices,
        "user": current_user
    }
    return render(request, 'policy-management.html', context)

def claims(request):
    current_user = request.user
    
    context = {
        "user": current_user
    }
    return render(request, 'claims.html', context)

def add_claims(request):
    policy = InsurancePolicy.objects.all()
    
    if request.method == "POST":
        pass
    
    context = {
        "policy": policy
    }
    return render(request, 'add-claims.html', context)

def payment(request):
    return render(request, 'payment.html')

def view_payments(request):
    return render(request, 'view-payments.html')

def vehicle(request):
    current_user = request.user
    vehicles =  Vehicle.objects.all()
    user_vehicles = Vehicle.objects.filter(owner=request.user)
    users = User.objects.filter(is_superuser=False)
    
    if request.method == 'POST':
        if current_user.is_superuser:
            owner = request.POST.get("owner")
            make = request.POST.get("make")
            model = request.POST.get("model")
            year = request.POST.get("year")
            license_plate = request.POST.get("license_plate")
            
            if not owner:
                return JsonResponse({"success": False, "message": "Owner is required.."})
            
            owner = User.objects.get(id=owner)
            
            Vehicle.objects.create(
                owner=owner, make=make, model=model, year=year, license_plate=license_plate
            )
            
            return JsonResponse({"success": True, "message": "Vehicle Registered Successfully..."})
        else:
            owner = request.user.id
            make = request.POST.get("make")
            model = request.POST.get("model")
            year = request.POST.get("year")
            license_plate = request.POST.get("license_plate")
            
            owner = User.objects.get(id=owner)
            
            Vehicle.objects.create(
                owner=owner, make=make, model=model, year=year, license_plate=license_plate
            )
            
            return JsonResponse({"success": True, "message": "Vehicle Registered Successfully..."})
    
    context = {
        'vehicles': vehicles,
        "user": current_user,
        "users": users,
        "user_vehicles": user_vehicles
    }
    return render(request, 'vehicles.html', context)
