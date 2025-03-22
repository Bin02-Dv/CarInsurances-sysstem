from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name="landing"),
    path('register/', views.register, name="register"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('dash/', views.dash, name="dash"),
    path('policy-management/', views.policy_management, name="policy-management"),
    path('add-policy/', views.add_policy, name="add-policy"),
    path('claims/', views.claims, name="claims"),
    path('add-claims/', views.add_claims, name="add-claims"),
    path('payment/', views.payment, name="payment"),
    path('view-payments/', views.view_payments, name="view-payments"),
    path('vehicle/', views.vehicle, name="vehicle"),
]