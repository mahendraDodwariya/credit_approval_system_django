# Credit Approval System Project in Django

## Overview

Welcome to the Credit Approval System project built with Django and Django Rest Framework. 

## Tech Stack

- **Django:** A high-level Python web framework that encourages rapid development and clean, pragmatic design.
- **Django Rest Framework (DRF):** A powerful and flexible toolkit for building Web APIs in Django applications.
- **Database:** PostgreSQL is used as the database to store customer and loan information.

## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Running the Application

To run the entire application and its dependencies, execute the following Docker Compose command:

```bash
docker-compose up --build
```

# API Functions

## 1. Register a Customer

**Endpoint:** `/api/customers/register/`

**Method:** `POST`

**Description:** Register a new customer with relevant details.

## 2. Check Loan Eligibility of Customer

**Endpoint:** `/api/customers/check-eligibility/`

**Method:** `POST`

**Description:** Check the loan eligibility of a customer based on specified criteria.

## 3. Create a Loan for Customer

**Endpoint:** `/api/loans/create-loan/`

**Method:** `POST`

**Description:** Create a new loan for a registered customer.

## 4. View Loan by Loan ID

**Endpoint:** `/api/loans/view-loan/<loan_id>/`

**Method:** `GET`

**Description:** View detailed information about a specific loan using its unique identifier.

## 5. View Loans of a Customer

**Endpoint:** `/api/loans/view-loans/<customer_id>/`

**Method:** `GET`

**Description:** Retrieve a list of loans associated with a specific customer.

