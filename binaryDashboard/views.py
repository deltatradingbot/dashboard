from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from .signals import *
from datetime import datetime
from django.conf import settings
import pytz
from django.contrib.auth.models import User
from authApp.models import PaymentModal


def IndexPage(request):
    return render(request, 'index.html')

def DashboardPage(request):
    if request.user.is_authenticated:
        user_id = User.objects.get(email=request.user.email).pk
        payObj = PaymentModal.objects.filter(user_id=user_id)
        if not payObj.exists():
            return render(request, 'dashboard-locked.html')
        elif not payObj[0].verified:
            return render(request, 'dashboard-locked.html')
    else:
        return redirect('/auth/login')
    lines = []
    with open(os.path.join(settings.BASE_DIR,'signal_history.txt'), 'r') as file:
        for line in file:
            l = {}
            l["t"] = line.split("-:-")[0]
            l['s'] = line.split("-:-")[1]
            l['dir'] = l['s'].split(" ")[0].lower()
            lines.append(l)
        
    data = {
        "lines" : lines
    }
    return render(request,'dashboard.html',data)

def RulesPage(request):
    if request.user.is_authenticated:
        user_id = User.objects.get(email=request.user.email).pk
        payObj = PaymentModal.objects.filter(user_id=user_id)
        if not payObj.exists():
            return render(request, 'dashboard-locked.html')
        elif not payObj[0].verified:
            return render(request, 'dashboard-locked.html')
    else:
        return redirect('/auth/login')
    return render(request,'rules.html')

def DisclaimerPage(request):
    if request.user.is_authenticated:
        user_id = User.objects.get(email=request.user.email).pk
        payObj = PaymentModal.objects.filter(user_id=user_id)
        if not payObj.exists():
            return render(request, 'dashboard-locked.html')
        elif not payObj[0].verified:
            return render(request, 'dashboard-locked.html')
    else:
        return redirect('/auth/login')
    return render(request,'disclaimer.html')

def SignalsAPI(request):
    if request.user.is_authenticated:
        user_id = User.objects.get(email=request.user.email).pk
        payObj = PaymentModal.objects.filter(user_id=user_id)
        if not payObj.exists():
            return render(request, 'dashboard-locked.html')
        elif not payObj[0].verified:
            return render(request, 'dashboard-locked.html')
    else:
        return redirect('/auth/login')
    instrument = "EUR_USD"
    granularity = "M5"
    res = run(instrument,granularity)

    ist_timezone = pytz.timezone('Asia/Kolkata')
    datetime.now(ist_timezone)
    t = datetime.now(ist_timezone).strftime("%Y-%m-%d %H:%M:%S")

    if res != "Wait for next signal.......":
        with open(os.path.join(settings.BASE_DIR,'signal_history.txt'), 'a') as file:
            file.write(t + "-:-" + res + "\n")
    
    data = {
        "status" : "success",
        "data" : {"signal" : res, "time" : t,'dir' : res.split(" ")[0].lower()}
    }
    return JsonResponse(data)
