from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Customer , Loan
from django.core.serializers import serialize
from .serializers import CustomerSerializer, LoanSerializerAll , LoanSerializer
from .helper import *
from datetime import date , timedelta
from decimal import Decimal
import json
from django.db import IntegrityError
import logging



@api_view(['POST'])
def register_customer(request ):
    serializer = CustomerSerializer(data=request.data)
    if serializer.is_valid():
        data = serializer.validated_data
        monthly_salary = data['monthly_salary']

        # Calculate approved limit based on the given formula
        approved_limit = round(36 * monthly_salary / 100000) * 100000

        # Create a new customer
        customer = Customer.objects.create(
            # customer_id=data['customer_id'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            age=data['age'],
            monthly_salary=monthly_salary,
            approved_limit=approved_limit,
            phone_number=data.get('phone_number', ''),
        )

        response_data = {
            'customer_id': customer.customer_id,
            'name': f"{customer.first_name} {customer.last_name}",
            'age': customer.age,
            'monthly_income': customer.monthly_salary,
            'approved_limit': customer.approved_limit,
            'phone_number': customer.phone_number
        }

        return Response(response_data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def view_loan(request, loan_id):
    try:
        loan = Loan.objects.get(pk=loan_id)
    except Loan.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    loan_serialized = LoanSerializerAll(loan)
    customer_serialized = CustomerSerializer(loan.customer)
    customer_data = dict(customer_serialized.data)
    loan_serialized.data["customer"] = customer_data 
    return Response(loan_serialized.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def create_loan(request):
    data = request.data
    customer_id = data['customer_id']
    interest_rate = data['interest_rate']
    loan_amount = data['loan_amount']
    tenure = data['tenure']
    message = "Approved"

    try:
        customer = Customer.objects.get(pk=customer_id)
        approval, corrected_interest = check_loan_eligibility(customer_id, interest_rate)
        # print(approval)
    except Customer.DoesNotExist:
        return Response({"message": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)

    monthly_installment = 0

    if approval:
        monthly_installment = calculate_monthly_installment(loan_amount, corrected_interest, tenure)

    response_data = {
        "loan_id": 0,
        "customer_id": customer_id,
        "loan_approved": approval,
        "message": message if approval else "Not approved",
        "monthly_installment": monthly_installment if approval else None,
    }
    try:

        if approval:
            new_loan = Loan.objects.create(
                customer=customer,
                loan_amount=loan_amount,
                interest_rate=corrected_interest,
                tenure=tenure,
                monthly_repayment=monthly_installment,
                start_date=date.today(),
                end_date=date.today() + timedelta(days=30 * tenure),
                repayments_left=tenure
            )

            response_data["loan_id"] = new_loan.loan_id
        return Response(response_data, status=status.HTTP_200_OK)

    except IntegrityError as e:
        logging.error(f"Error creating loan: {e}")
        return Response({"message": "Error creating loan"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def checkEligibility(request):
    data = request.data
    customer_id  = data['customer_id']
    interest_rate  = data['interest_rate']
    loan_amount  = data['loan_amount']
    tenure  = data['tenure']

    monthly_installment = 0


    if customer_id:
        customer = Customer.objects.get(pk=customer_id)
        loans = Loan.objects.filter(customer=customer)
        credit_score = get_creditS_score(customer_id)
        sum_of_emis = 0
        corrected_interest = interest_rate

        if sum_of_emis > customer.monthly_salary:
            approval = False
        else:   
            if credit_score >= 50:
                approval = True
            elif 50 > credit_score >= 30:
                approval = True
                corrected_interest = max(12 , interest_rate)
            elif 30 > credit_score >= 10:
                approval = True
                corrected_interest = max(16 , interest_rate)
            else:
                approval = False

        if approval == True:
            monthly_installment = calculate_monthly_installment( loan_amount , corrected_interest,tenure)

        response_data = {
            "customer_id":customer_id,
            "approval":approval,
            "interest_rate":interest_rate,
            "corrected_interest_rate": corrected_interest,
            "tenure":tenure,
            "monthly_installment":monthly_installment,
        }

    return Response(response_data, status=status.HTTP_200_OK)



@api_view(['GET'])
def view_loans_by_customer_id(request, customer_id):
    try:
        customer = Customer.objects.get(customer_id = customer_id)
        loans = Loan.objects.filter(customer = customer)

        # Return response
        result = []

        for loan in loans:
            result.append(LoanSerializer(loan).data)
        return Response(result, status=status.HTTP_200_OK)
    except Customer.DoesNotExist:
        return Response({'message': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)