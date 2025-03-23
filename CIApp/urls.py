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
    path('api/policies/', views.get_policy_details, name='get_policy_details'),
    
    # update
    path('approved/<int:id>/', views.approved, name="approved"),
    path('rejected/<int:id>/', views.rejected, name="rejected"),
    path('delete-claim/<int:id>/', views.delete_claim, name="delete-claim"),
    path('delete-policy/<int:id>/', views.delete_policy, name="delete-policy"),
]