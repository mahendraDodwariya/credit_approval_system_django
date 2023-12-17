import random
from .models import Customer , Loan
from datetime import datetime
from django.utils import timezone
from datetime import datetime

def get_creditS_score(customer):
    loans = Loan.objects.filter(customer=customer)
    total_loans = loans.count()

    if total_loans == 0:
        return 50  # No loans, consider a base credit score

    total_paid_on_time = sum(loan.emis_paid_on_time for loan in loans)
    total_loan_amount = sum(loan.loan_amount for loan in loans)

    # Calculate the percentage of EMIs paid on time
    percentage_paid_on_time = (total_paid_on_time / (total_loans)) * 100

    # Calculate credit score based on various factors
    credit_score = calculate_credit_score(percentage_paid_on_time, total_loan_amount)

    return credit_score

def calculate_credit_score(percentage_paid_on_time, total_loan_amount):
    # You can define your own credit scoring logic based on the provided factors
    # This is just a simple example, you might want to fine-tune it based on your requirements

    weight_percentage_paid_on_time = 0.7
    weight_total_loan_amount = 0.3

    normalized_percentage_paid_on_time = percentage_paid_on_time / 100
    normalized_total_loan_amount = total_loan_amount / 100000  # Assuming a maximum loan amount of 100,000

    weighted_sum = (
        weight_percentage_paid_on_time * normalized_percentage_paid_on_time +
        weight_total_loan_amount * normalized_total_loan_amount
    )

    # Map the weighted sum to the credit rating scale (0 to 100)
    credit_score = int(weighted_sum * 100)

    # Ensure credit score is within the valid range (0 to 100)
    credit_score = max(0, min(100, credit_score))

    return credit_score




def get_creditS_score(customer_id):
    customer = Customer.objects.get(pk = customer_id)
    loans = Loan.objects.filter(customer=customer)
    for loan in loans:
        pass
    return random.randint(0, 100)



def calculate_monthly_installment(principal, interest_rate, tenure):
    monthly_interest_rate = interest_rate / 1200
    # Check for zero denominator
    if (1 + monthly_interest_rate) ** tenure - 1 == 0:
        return 0  # You can return a default value or handle it as needed
    monthly_emis = principal * ((( monthly_interest_rate * (1 + monthly_interest_rate)**tenure)) / ((1 + monthly_interest_rate)**tenure - 1))
    rounded_monthly_emis = round(monthly_emis , 2)
    return rounded_monthly_emis
    

def past_loan_completed_on_time(customer):
    # customer = Customer.objects.get(id=customer)
    # loans = Loan.objects.filter(customer__id=customer.id)
    loans = Loan.objects.filter(customer=customer)
    loan_approved_volume=0
    total_loan_taken =0
    loans_in_current_year =0
    if not loans.exists():
       return 100,loan_approved_volume,total_loan_taken,loans_in_current_year,0
    
    # find today's date and check each loan if completed  then check with tenure
    
    current_year = datetime.now().year
    curr_date = timezone.now().date()
    loans_in_current_year = loans.filter(start_date__year=current_year).count()
    total_loan = 0
    paid_on_time = 0
    loan_approved_volume=0
    sum_of_current_loan =0

    for loan in loans:
        total_loan_taken+=1
        sum_of_current_loan = loan.tenure- loan.emis_paid_on_time
        loan_approved_volume+=loan.loan_amount
        if loan.end_date < curr_date:
            total_loan += 1
            if loan.emis_paid_on_time == loan.tenure:
                paid_on_time += 1
        else:
            sum_of_current_loan+=loan.loan_amount
 

    # Calculate the percentage of loans paid on time
    if total_loan > 0:
        percentage_paid_on_time = (paid_on_time / total_loan) * 100
    else:
        percentage_paid_on_time = 0
    
    if total_loan ==0:
        return 100,loan_approved_volume,total_loan_taken,loans_in_current_year,sum_of_current_loan
    return percentage_paid_on_time,loan_approved_volume,total_loan_taken,loans_in_current_year,sum_of_current_loan

        


def check_loan_eligibility(customer_id, interest_rate):
    try:
        customer = Customer.objects.get(pk=customer_id)
    except Customer.DoesNotExist:
        return False, 0  # Customer not found, loan not approved

    percentage_paid_on_time, loan_approved_volume, total_loan_taken, loans_in_current_year, sum_current_emis = past_loan_completed_on_time(customer)
    
    weight_percentage_paid_on_time = 0.4
    weight_loan_approved_volume = 0.2  # Inversely proportional
    weight_total_loan_taken = 0.2  # Inversely proportional
    weight_loans_in_current_year = 0.2  # Inversely proportional

    # Define the maximum expected values for inversely proportional parameters
    max_loan_approved_volume = 100000  # Replace with the actual maximum value
    max_total_loan_taken = 50  # Replace with the actual maximum value
    max_loans_in_current_year = 12  # Replace with the actual maximum value

    # Normalize the values to be between 0 and 1
    normalized_percentage_paid_on_time = percentage_paid_on_time / 100
    normalized_loan_approved_volume = 1 - (loan_approved_volume / max_loan_approved_volume)
    normalized_total_loan_taken = 1 - (total_loan_taken / max_total_loan_taken)
    normalized_loans_in_current_year = 1 - (loans_in_current_year / max_loans_in_current_year)

    # Calculate the weighted sum of normalized values
    weighted_sum = (
        float(weight_percentage_paid_on_time) * float(normalized_percentage_paid_on_time) +
        float(weight_loan_approved_volume) * float(normalized_loan_approved_volume) +
        float(weight_total_loan_taken) * float(normalized_total_loan_taken) +
        float(weight_loans_in_current_year) * float(normalized_loans_in_current_year)
    )

    # Map the weighted sum to the credit rating scale (0 to 100)
    credit_rating = int(weighted_sum * 100)

    # Ensure credit rating is within the valid range (0 to 100)
    credit_rating = max(0, min(100, credit_rating))

    # Implement credit approval logic
    if credit_rating > 50:
        approval = True
        corrected_interest_rate = interest_rate
    elif 50 > credit_rating > 30:
        if interest_rate > 12:
            approval = True
            corrected_interest_rate = interest_rate
        else:
            approval = False
            corrected_interest_rate = 12
    elif 30 > credit_rating > 10:
        if interest_rate > 16:
            approval = True
            corrected_interest_rate = interest_rate
        else:
            approval = False
            corrected_interest_rate = 16
    else:
        approval = False
        corrected_interest_rate = 0  # No loan approved if credit rating is less than 10

    # Additional checks
    if sum_current_emis > (0.5 * float(customer.monthly_salary)):
        approval = False
        corrected_interest_rate = 0  # Reset interest rate if total EMIs exceed 50% of monthly salary

    return approval, corrected_interest_rate
