from django.db import models
from django.contrib.auth import get_user_model

# Custom User Model with Role-Based Access
User = get_user_model()


# Insurance Policy Model
class InsurancePolicy(models.Model):
    POLICY_TYPES = [
        ('third-party', 'Third-Party'),
        ('comprehensive', 'Comprehensive'),
    ]

    policy_name = models.CharField(max_length=100)
    policy_type = models.CharField(max_length=20, choices=POLICY_TYPES)
    coverage_details = models.TextField()
    premium_amount = models.DecimalField(max_digits=10, decimal_places=2)
    duration_months = models.PositiveIntegerField()  # Policy duration in months

    def __str__(self):
        return self.policy_name


# Vehicle Model
class Vehicle(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    license_plate = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.make} {self.model} ({self.license_plate})"


# Claim Model
class Claim(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    policy = models.ForeignKey(InsurancePolicy, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    incident_date = models.DateField()
    claim_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    supporting_documents = models.FileField(upload_to='claims/documents/', blank=True, null=True)

    def __str__(self):
        return f"Claim by {self.user.username} - {self.status}" 


# Payment Model
class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    policy = models.ForeignKey(InsurancePolicy, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    transaction_reference = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"Payment {self.transaction_reference} - {self.amount}"
