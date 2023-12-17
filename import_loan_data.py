# import_loan_data.py

import os
import django
import pandas as pd

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'credit_approval_system.settings')

# Configure Django settings
django.setup()

from credit_approval.models import Customer,Loan

# Read data from the Excel file
df = pd.read_excel('loan_data.xlsx')

# Iterate through rows and save data to Loan model
for index, row in df.iterrows():
    # Find the customer based on the provided Customer ID
    customer_id = row['Customer ID']
    try:
        customer = Customer.objects.get(customer_id=customer_id)
    except Customer.DoesNotExist:
        print(f"Customer with ID {customer_id} not found. Skipping.")
        continue

    loan = Loan(
        loan_id = row['Loan ID'],
        customer=customer,
        loan_amount=row['Loan Amount'],
        interest_rate=row['Interest Rate'],
        tenure=row['Tenure'],
        emis_paid_on_time=row['EMIs paid on Time'],
        start_date=row['Date of Approval'],
        end_date=row['End Date'],
        monthly_repayment = 0,
    )
    loan.save()
