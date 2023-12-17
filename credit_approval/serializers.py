from rest_framework import serializers
from .models import Customer , Loan

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'phone_number', 'monthly_salary' , 'age']
        # Exclude approved_limit and current_debt


class LoanSerializerAll(serializers.ModelSerializer):
    customer = CustomerSerializer()
    class Meta:
        model = Loan
        fields = ['loan_id','customer','loan_amount','interest_rate','monthly_repayment','tenure']

class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        exclude = ['emis_paid_on_time', 'start_date', 'end_date','customer','tenure']