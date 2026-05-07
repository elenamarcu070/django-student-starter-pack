# Django Student Starter Pack

A complete Django booking system starter template built for university projects, portfolio apps and reservation systems.

---

## Features

- Modern Django project structure
- Google OAuth authentication
- Email/password authentication
- Booking system with time slots
- Resource management
- Dashboard UI
- Admin panel
- Bootstrap 5 responsive design
- Railway deployment ready
- Demo seed data included
- PostgreSQL ready

---

## Tech Stack

- Python
- Django
- Bootstrap 5
- PostgreSQL
- django-allauth
- Railway
- Gunicorn

---

# Screenshots

## Homepage
(Add screenshot here)

## Dashboard
(Add screenshot here)

## Booking System
(Add screenshot here)

## Admin Panel
(Add screenshot here)

---

# Installation

## 1. Clone repository

```bash
git clone YOUR_REPOSITORY_URL
```

---

## 2. Create virtual environment

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### Mac/Linux

```bash
source venv/bin/activate
```

---

## 3. Install requirements

```bash
pip install -r requirements.txt
```

---

## 4. Run migrations

```bash
python manage.py migrate
```

---

## 5. Create superuser

```bash
python manage.py createsuperuser
```

---

## 6. Load demo data

```bash
python manage.py seed_demo
```

---

## 7. Run server

```bash
python manage.py runserver
```

---

# Google OAuth Setup

Go to Google Cloud Console and create OAuth credentials.

Add these redirect URIs:

```text
http://127.0.0.1:8000/accounts/google/login/callback/
```

```text
http://localhost:8000/accounts/google/login/callback/
```

Then configure the credentials inside Django Admin:

```text
/admin/socialaccount/socialapp/
```

---

# Deployment

This project is ready for deployment on:

- Railway
- Render
- VPS
- Docker

---

# Included Demo Features

- Demo locations
- Demo resources
- Booking system
- Responsive dashboard
- Admin management

---

# License

This project is for educational and commercial usage.
