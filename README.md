<div align="center">

# 🍽️ KhanayWala AI

### AI-Powered Food Delivery Platform

Built with **Python**, **FastAPI**, **PostgreSQL**, and **Mistral AI**

A modern food delivery platform where customers can discover restaurants, receive AI-powered meal recommendations, place orders, and track deliveries, while restaurant owners manage menus and admins oversee platform operations.

<p>

<img src="https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>

<img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white"/>

<img src="https://img.shields.io/badge/PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white"/>

<img src="https://img.shields.io/badge/Mistral-AI-orange?style=for-the-badge"/>

<img src="https://img.shields.io/badge/Railway-0B0D0E?style=for-the-badge&logo=railway&logoColor=white"/>

<img src="https://img.shields.io/badge/React-Planned-61DAFB?style=for-the-badge&logo=react"/>

</p>

</div>

---

# 🚀 Overview

KhanayWala AI is a production-style food delivery backend designed with modern backend engineering principles.

The platform enables customers to discover restaurants, order food, receive AI-powered meal recommendations, and track their orders while restaurant owners manage menus and administrators monitor the platform through analytics dashboards.

This project demonstrates scalable backend architecture, role-based authentication, AI integration, and REST API development using Python and FastAPI.

---

# ✨ Key Features

## 🔐 Authentication

- JWT Authentication
- Access & Refresh Tokens
- Role-Based Authorization
- Secure Password Hashing

### User Roles

- 👤 Customer
- 🍽 Restaurant Owner
- 👨‍💼 Administrator

---

## 🍽 Restaurant Management

- Restaurant Registration
- Restaurant Approval Workflow
- Categories
- Restaurant Profiles
- Search Restaurants

---

## 🍕 Menu Management

- Menu CRUD
- Food Categories
- Image Support
- Price Management
- Search Menu Items

---

## 🛒 Smart Ordering

- Single Restaurant Cart
- Quantity Management
- Automatic Price Calculation
- Checkout
- Order History

---

## 📦 Order Tracking

Order lifecycle:

```text
Pending
   │
Preparing
   │
Out for Delivery
   │
Delivered

or

Cancelled
```

---

## 🤖 AI Food Assistant

Powered by **Mistral AI**

The assistant can:

- Recommend meals
- Suggest foods within a budget
- Recommend cuisines
- Personalize food choices
- Maintain conversation context

---

## ⭐ Reviews & Ratings

- Verified Purchase Reviews
- One Review Per Delivered Order
- Ratings
- Customer Feedback

---

## 📊 Analytics Dashboard

### Admin Dashboard

- Total Users
- Total Restaurants
- Total Orders
- Revenue Analytics
- Platform Insights

### Restaurant Dashboard

- Revenue
- Orders
- Best Selling Foods
- Sales Analytics

---

# 🏗 System Architecture

```text
                    Client Applications
                           │
                           ▼
                    FastAPI REST API
                           │
      ┌──────────────┬───────────────┬─────────────┐
      │              │               │
 Authentication   Restaurant API   AI Assistant
      │              │               │
      └──────────────┼───────────────┘
                     │
              Business Services
                     │
                     ▼
                 PostgreSQL
```

---

# 🛠 Technology Stack

| Category | Technologies |
|-----------|--------------|
| Language | Python 3.12 |
| Framework | FastAPI |
| ORM | SQLAlchemy |
| Database | PostgreSQL (Neon) |
| Validation | Pydantic |
| Authentication | JWT |
| AI | Mistral AI |
| Migrations | Alembic |
| Deployment | Railway |
| Frontend | React (Planned) |

---

# 📂 Project Structure

```bash
khanaywala-ai/
│
├── app/
│   ├── api/
│   ├── auth/
│   ├── core/
│   ├── crud/
│   ├── db/
│   ├── models/
│   ├── schemas/
│   ├── ai/
│   ├── migrations/
│   └── main.py
│
├── requirements.txt
├── alembic.ini
├── .env.example
└── README.md
```

---

# ⚡ Quick Start

## Clone Repository

```bash
git clone https://github.com/abizaid24/khanaywala-ai.git

cd khanaywala-ai
```

---

## Create Virtual Environment

### Windows

```powershell
python -m venv .venv

.\.venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv .venv

source .venv/bin/activate
```

---

## Install Dependencies

```bash
pip install --upgrade pip

pip install -r requirements.txt
```

---

## Configure Environment

Create a `.env` file.

```env
DATABASE_URL=

SECRET_KEY=

MISTRAL_API_KEY=

MISTRAL_MODEL=

FRONTEND_URL=
```

---

## Run Database Migrations

```bash
alembic upgrade head
```

---

## Start Server

```bash
uvicorn app.main:app --reload
```

Server:

```
http://127.0.0.1:8000
```

Swagger Documentation:

```
http://127.0.0.1:8000/docs
```

---

# 👥 User Roles

## 👤 Customer

- Browse Restaurants
- AI Meal Recommendations
- Place Orders
- Track Deliveries
- Reviews & Ratings

---

## 🍽 Restaurant Owner

- Register Restaurant
- Manage Menu
- Receive Orders
- Analytics Dashboard

---

## 👨‍💼 Administrator

- Approve Restaurants
- Manage Users
- Revenue Analytics
- Platform Management

---

# 📸 Screenshots

Add screenshots here:

- Home Page
- Restaurant Listing
- Restaurant Dashboard
- Admin Dashboard
- AI Food Assistant
- Swagger API
- Order Tracking

---

# 🚀 Roadmap

### ✅ Completed

- JWT Authentication
- Restaurant Management
- Menu Management
- Shopping Cart
- Ordering System
- AI Food Assistant
- Analytics Dashboard

### 🔜 Planned

- React Frontend
- Stripe Payments
- Live Order Tracking
- Push Notifications
- Google Maps Integration
- Docker Deployment
- CI/CD Pipeline
- Recommendation Engine Improvements

---

# 🌟 Why KhanayWala AI?

KhanayWala AI demonstrates production-ready backend engineering by combining secure authentication, scalable REST APIs, AI-powered recommendations, modular architecture, and role-based workflows into a modern food delivery platform.

This project showcases backend development best practices using Python and FastAPI while integrating conversational AI into a real-world business application.

---

# 📄 License

Licensed under the MIT License.

---

# 👨‍💻 Author

## Hafiz Abi Zaid

**Python Backend Developer • FastAPI • Agentic AI**

📧 **hafizabizaid@gmail.com**

🌐 **https://github.com/abizaid24**

---

<div align="center">

### ⭐ If you found this project useful, consider giving it a Star!

Building scalable backend systems with Python, FastAPI & AI.

</div>
