from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login, logout
from .models import PaymentModal
from datetime import datetime

# Create your views here.
def LoginPage(request):
    if request.user.is_authenticated:
        user_id = User.objects.get(username=request.user).pk
        payObj = PaymentModal.objects.filter(user_id=user_id)
        if not payObj.exists():
            return render(request, 'dashboard-locked.html')
        elif not payObj[0].verified:
            return render(request, 'dashboard-locked.html')
        return redirect('/dashboard')
    if request.method == "POST":
        email = request.POST.get('email')
        password =request.POST.get('pass')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('/dashboard')
        else:
            messages.error(request, "Login Failed!")
            return render(request, 'login.html')
    return render(request, 'login.html')

def LogoutView(request):
    logout(request)
    return redirect('/auth/login')

def RegisterPage(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        pwrd = request.POST['pass']
        pwrd2 = request.POST['pass2']
        if pwrd != pwrd2:
            messages.error(request, "Password doesn't match.")
        try:
            user = User.objects.create_user(username = email , password=pwrd)
            messages.success(request, "Congrats! You are registered successfully.")
            return redirect('/auth/login')
        except:
            messages.error(request, "User already registered!!")

    return render(request, 'register.html')

def PaymentPage(request):
    if request.method == "POST":
        if request.POST['ref']:
            user_id = User.objects.get(username=request.user).pk
            my_instance = PaymentModal(user_id=user_id, pay_id=request.POST['ref'],latest_pay=datetime.now())
            my_instance.save()
            return redirect('/auth/pay-verify')
        else:
            messages.error(request, "Invalid UPI ref number.")
    return render(request, 'payment.html')

def PaymentVerificationPage(request):
    return render(request, 'payment-verify.html')