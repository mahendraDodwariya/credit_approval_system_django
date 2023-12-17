from django.db import models
from decimal import Decimal, ROUND_HALF_EVEN
from django.core.validators import MinValueValidator, MaxValueValidator

class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    age = models.PositiveIntegerField(null=True)
    phone_number = models.CharField(max_length=20)
    monthly_salary = models.DecimalField(max_digits=10, decimal_places=2)
    approved_limit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    current_debt = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.customer_id})"


class Loan(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    loan_id = models.AutoField(primary_key=True)
    loan_amount = models.DecimalField(max_digits=10, decimal_places=2)
    tenure = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(240)])
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    monthly_repayment = models.DecimalField(max_digits=10, decimal_places=2)
    emis_paid_on_time = models.PositiveIntegerField(default=0)
    start_date = models.DateField()
    end_date = models.DateField()
    repayments_left = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Loan #{self.loan_id} for {self.customer}"

