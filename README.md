# Event Workshop Registration & Management System

## 1. Project Overview

The Event Workshop Registration & Management System is a full-stack web application for managing workshops, participant registrations, and online payments.

The system has two roles:

- Participant
- Admin

### Participant Features

- Register account
- Login
- Browse workshops
- Search workshops
- View workshop details
- Register for a workshop
- Make Stripe payment
- View registrations
- Cancel registration
- Receive email notifications

### Admin Features

- Admin registration and login
- Create workshops
- Update workshops
- Delete workshops
- Manage workshop capacity
- View participants
- View payments
- View total revenue
- View dashboard statistics

---

# 2. Technology Stack

## Backend

- Python
- FastAPI
- SQLAlchemy
- MySQL
- JWT Authentication
- Passlib/Bcrypt
- Stripe
- SMTP Email
- Pytest

## Frontend

- React
- Vite
- React Router
- Axios
- Tailwind CSS
- React Toastify

---

# 3. Project Structure

```text
Event Workshop/
│
├── backend/
│   ├── app/
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── workshop.py
│   │   │   ├── registration.py
│   │   │   └── payment.py
│   │   │
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── workshop.py
│   │   │   ├── registration.py
│   │   │   └── payment.py
│   │   │
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── workshops.py
│   │   │   ├── registrations.py
│   │   │   ├── payments.py
│   │   │   └── admin.py
│   │   │
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── stripe_service.py
│   │   │   └── email_service.py
│   │   │
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── database.py
│   │   ├── config.py
│   │   ├── security.py
│   │   └── dependency.py
│   │
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py
│   │   ├── test_auth.py
│   │   ├── test_workshops.py
│   │   ├── test_registrations.py
│   │   └── test_payments.py
│   │
│   ├── .env
│   ├── .env.example
│   ├── .gitignore
│   ├── requirements.txt
│   └── README.md
│
└── frontend/
    ├── src/
    │   ├── api/
    │   │   └── axios.js
    │   │
    │   ├── components/
    │   │   ├── Navbar.jsx
    │   │   └── ProtectedRoute.jsx
    │   │
    │   ├── pages/
    │   │   ├── Login.jsx
    │   │   ├── Register.jsx
    │   │   │
    │   │   ├── workshops/
    │   │   │   ├── WorkshopList.jsx
    │   │   │   └── WorkshopDetails.jsx
    │   │   │
    │   │   ├── registrations/
    │   │   │   ├── RegistrationList.jsx
    │   │   │   └── RegistrationDetails.jsx
    │   │   │
    │   │   ├── checkout/
    │   │   │   ├── Checkout.jsx
    │   │   │   ├── CheckoutSuccess.jsx
    │   │   │   └── CheckoutCancel.jsx
    │   │   │
    │   │   └── admin/
    │   │       ├── AdminDashboard.jsx
    │   │       ├── AdminWorkshops.jsx
    │   │       ├── AdminParticipants.jsx
    │   │       ├── AdminPayments.jsx
    │   │       └── AdminRevenue.jsx
    │   │
    │   ├── routes/
    │   │   └── AppRoutes.jsx
    │   ├── App.jsx
    │   ├── main.jsx
    │   └── index.css
    │
    ├── package.json
    └── vite.config.js

4. Database Configuration
Create the MySQL database:
CREATE DATABASE event_system;

The application uses the following tables:
users
workshops
registrations
payments

Users
Stores participant and admin accounts.
Workshops
Stores workshop information, capacity, available seats, price and status.
Registrations
Connects participants with workshops.
Payments
Stores Stripe payment information.
5. Environment Variables
Create a .env file inside the backend folder.
Example:
DATABASE_URL=mysql+pymysql://root:your_password@localhost:3306/event_system

SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

STRIPE_SECRET_KEY=your_stripe_secret_key
STRIPE_WEBHOOK_SECRET=your_stripe_webhook_secret

SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password
SMTP_FROM_EMAIL=your_email@gmail.com
SMTP_FROM_NAME=Event Workshop System

Do not commit the real .env file to GitHub.
Only .env.example should be submitted.
6. Backend Setup
Open terminal and go to the backend:
cd backend

Create a virtual environment:
python -m venv venv

Activate it on Windows:
venv\Scripts\activate

Install dependencies:
pip install -r requirements.txt

Start FastAPI:
uvicorn app.main:app --reload

Backend will run at:
http://127.0.0.1:8000

7. Swagger API Documentation
FastAPI automatically provides Swagger documentation.
Open:
http://127.0.0.1:8000/docs

The API contains:
- Authentication
- Workshops
- Registrations
- Payments
- Admin
Swagger can be used to test the backend APIs.
8. Frontend Setup
Open another terminal:
cd frontend

Install dependencies:
npm install

Start the React Vite application:
npm run dev

Frontend will run at:
http://localhost:5173

9. Stripe Configuration
The application uses Stripe in test mode.
Add the Stripe test secret key to .env:
STRIPE_SECRET_KEY=your_test_secret_key

Add the Stripe webhook secret:
STRIPE_WEBHOOK_SECRET=your_test_webhook_secret

The payment flow is:
Participant
    ↓
Select Workshop
    ↓
Register
    ↓
Create Stripe Checkout Session
    ↓
Stripe Test Checkout
    ↓
Successful Payment
    ↓
Stripe Webhook
    ↓
Payment = SUCCESS
    ↓
Registration = CONFIRMED
    ↓
Confirmation Email

Stripe test cards can be used for testing instead of real cards.
10. Email Configuration
The application uses SMTP for email notifications.
Gmail SMTP configuration:
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password
SMTP_FROM_EMAIL=your_email@gmail.com
SMTP_FROM_NAME=Event Workshop System

Email notifications are sent for:
Payment Confirmation
Sent after successful Stripe payment.
Registration Cancellation
Sent when a participant cancels a registration.
11. Authentication
The application uses JWT authentication.
After login, the backend generates an access token.
The frontend stores the token and sends it with protected API requests:
Authorization: Bearer <access_token>

Role-based access is implemented for:
Participant
Admin

12. Workshop Registration Flow
Participant Login
       ↓
Browse Workshops
       ↓
View Workshop
       ↓
Register
       ↓
Registration PENDING
       ↓
Stripe Checkout
       ↓
Payment SUCCESS
       ↓
Registration CONFIRMED

Workshop capacity is also managed.
When a participant registers:
available_seats = available_seats - 1

When a participant cancels:
available_seats = available_seats + 1

13. Testing
The project uses Pytest.
Run all tests:
pytest -v

Current test coverage includes:
1. User registration
2. User login
3. Invalid login
4. Workshop creation
5. Workshop pagination
6. Successful registration
7. Duplicate registration prevention
8. Full workshop prevention
9. Unauthorized registration access
10. Stripe checkout API

The tests also verify important business rules such as:
- Duplicate registration is prevented.
- Full workshops cannot accept registrations.
- Participants cannot access another participant's registration.
14. Frontend Routes
Public
/
 /login
 /register

Participant
/workshops
/workshops/:id
/registrations
/registrations/:id
/checkout
/checkout/success
/checkout/cancel

Admin
/admin/dashboard
/admin/workshops
/admin/participants
/admin/payments
/admin/revenue

15. Submission Checklist
Before submitting, verify:
- [ ] FastAPI backend
- [ ] React Vite frontend
- [ ] MySQL database
- [ ] SQLAlchemy models
- [ ] JWT authentication
- [ ] Stripe test-mode integration
- [ ] Stripe webhook
- [ ] Email integration
- [ ] Pytest test cases
- [ ] .env.example
- [ ] README.md
- [ ] Swagger/API documentation
- [ ] Stripe payment screenshots
- [ ] .env excluded from GitHub
16. Stripe Payment Evidence
Take screenshots showing:
1. Workshop registration
2. Stripe Checkout test page
3. Successful Stripe test payment
4. Payment status as SUCCESS
5. Registration status as CONFIRMED
6. Payment success page
These screenshots should be included as submission evidence.
17. Final Run Commands
Backend
cd backend
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload

Frontend
cd frontend
npm install
npm run dev

Tests
cd backend
pytest -v

Swagger
http://127.0.0.1:8000/docs

Frontend
http://localhost:5173    