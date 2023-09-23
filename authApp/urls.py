from django.urls import path
from .views import *

urlpatterns = [

    path('login',LoginPage,name='login'),
    path('logout',LogoutView,name='logout'),
    path('register',RegisterPage,name='register'),
    path('pay',PaymentPage,name='pay'),
    path('pay-verify',PaymentVerificationPage,name='payverify'),
]
