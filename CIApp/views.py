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

@login_required(login_url='/login')
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

@login_required(login_url='/login')
def policy_management(request):
    current_user = request.user
    polices =  InsurancePolicy.objects.all()
    
    context = {
        'polices': polices,
        "user": current_user
    }
    return render(request, 'policy-management.html', context)

@login_required(login_url='/login')
def claims(request):
    current_user = request.user
    claims = Claim.objects.filter(user=current_user)
    
    context = {
        "user": current_user,
        "claims": claims
    }
    return render(request, 'claims.html', context)

@login_required(login_url='/login')
def add_claims(request):
    user = request.user
    policy = InsurancePolicy.objects.all()
    vehicles = Vehicle.objects.filter(owner=user)

    if request.method == "POST":
        try:
            if not request.FILES.get('supporting_docs'):
                return JsonResponse({"success": False, "message": "Supporting Documents are required!!"})
            
            policy_id = request.POST.get('policy')
            vehicle_id = request.POST.get('vehicle')
            incident_date = request.POST.get('incident_date')
            claim_amount = request.POST.get('claim_amount')
            supporting_docs = request.FILES.get('supporting_docs')
            
            selected_policy = InsurancePolicy.objects.get(id=policy_id)
            selected_vehicle = Vehicle.objects.get(id=vehicle_id)

            Claim.objects.create(
                user=user,
                policy=selected_policy,
                vehicle=selected_vehicle,
                incident_date=incident_date,
                claim_amount=claim_amount, 
                supporting_documents=supporting_docs
            )
            
            return JsonResponse({"success": True, "message": "Claim Sent successfully..."})

        except InsurancePolicy.DoesNotExist:
            return JsonResponse({"success": False, "message": "Selected policy not found!"})
        except Vehicle.DoesNotExist:
            return JsonResponse({"success": False, "message": "Selected vehicle not found!"})
        except Exception as e:
            return JsonResponse({"success": False, "message": f"Error: {str(e)}"})

    context = {
        "policy": policy,
        "vehicles": vehicles,
    }
    return render(request, 'add-claims.html', context)

@login_required(login_url='/login')
def payment(request):
    return render(request, 'payment.html')

@login_required(login_url='/login')
def view_payments(request):
    return render(request, 'view-payments.html')

@login_required(login_url='/login')
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
