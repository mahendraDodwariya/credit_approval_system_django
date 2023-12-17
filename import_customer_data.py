# import_customer_data.py

import os
import django
import pandas as pd

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'credit_approval_system.settings')

# Configure Django settings
django.setup()

from credit_approval.models import Customer

# Read data from the Excel file
df = pd.read_excel('customer_data.xlsx')

# Iterate through rows and save data to Customer model
for index, row in df.iterrows():
    customer = Customer(
        first_name=row['First Name'],
        last_name=row['Last Name'],
        age=row['Age'],
        monthly_salary=row['Monthly Salary'],
        phone_number=row['Phone Number'],
        approved_limit=row['Approved Limit'],
    )
    customer.save()
