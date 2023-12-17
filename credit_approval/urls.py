from django.urls import path
from .views import *


urlpatterns = [
    path('register/', register_customer, name='register'),
    path('check-eligibility/', checkEligibility, name='check_eligibility'),
    path('create-loan/', create_loan, name='create_loan'),
    path('view-loan/<loan_id>/', view_loan, name='view_loan'),
    path('view-loans/<customer_id>/', view_loans_by_customer_id, name='view_loans'),
]