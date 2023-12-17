
FROM python:3.11.4-slim-buster

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
COPY customer_data.xlsx customer_data.xlsx
COPY import_loan_data.py import_loan_data.py

RUN pip install -r requirements.txt

# copy project
COPY . .