python manage.py makemigrations --no-input
python manage.py migrate --no-input
python import_customer_data.py
python import_loan_data.py
echo "from django.contrib.auth.models import User; User.objects.create_superuser('m', '', 'm')" | python3 manage.py shell

python manage.py runserver 0.0.0.0:8000