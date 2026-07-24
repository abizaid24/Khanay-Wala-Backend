# 🍽️ KhanayWala AI

> AI-Powered Food Delivery Platform built with **FastAPI, PostgreSQL, React, and Mistral AI**

KhanayWala AI is a modern food delivery platform where restaurant owners can list and manage their restaurants while customers can discover food, place orders, receive AI-powered meal recommendations, and track their orders in real time.

The platform also includes role-based authentication, restaurant approval workflows, analytics dashboards, verified reviews, and an intelligent AI assistant that helps users discover meals based on their preferences and budget.

---

# ✨ Features

## 👤 Authentication

- JWT Authentication
- Refresh Tokens
- Role-Based Authorization
- Customer
- Restaurant Owner
- Admin

---

## 🍔 Restaurant Management

- Restaurant Registration
- Admin Approval Workflow
- Restaurant Search
- Categories
- Restaurant Profiles

---

## 🍕 Menu Management

- Food Categories
- Menu CRUD
- Food Images
- Pricing
- Search Foods

---

## 🛒 Shopping Cart

- Single Restaurant Cart
- Quantity Management
- Automatic Price Calculation
- Checkout

---

## 📦 Order Management

- Place Orders
- Order History
- Live Status Tracking

Order Flow

Pending

↓

Preparing

↓

Out for Delivery

↓

Delivered

or

Cancelled

---

## 🤖 AI Food Assistant

Powered by **Mistral AI**

The AI Assistant can:

- Recommend meals
- Suggest food by budget
- Recommend cuisines
- Help customers choose meals
- Remember previous conversation context

---

## ⭐ Reviews

Verified Purchase Reviews

- Ratings
- Comments
- One Review Per Delivered Order

---

## 📊 Analytics Dashboard

### Admin Dashboard

- Total Users
- Total Restaurants
- Total Orders
- Revenue Analytics
- Restaurant Management
- User Management

### Restaurant Dashboard

- Revenue
- Orders
- Best Selling Foods
- Sales Analytics

---

# 🛠 Tech Stack

## Backend

- FastAPI
- SQLAlchemy
- Alembic
- PostgreSQL
- JWT Authentication
- Pydantic

## AI

- Mistral AI API

## Database

- PostgreSQL (Neon)

## Deployment

- Railway

## Frontend (Planned)

- React
- Vite
- TailwindCSS
- Shadcn UI

---

# 📁 Project Structure

```
app/
│
├── api/
├── auth/
├── core/
├── crud/
├── db/
├── models/
├── schemas/
├── ai/
├── migrations/
└── main.py
```

---

# ⚙️ Installation

Clone Repository

```bash
git clone https://github.com/yourusername/khanaywala-ai.git

cd khanaywala-ai
```

Create Virtual Environment

```bash
python -m venv venv
```

Activate

Windows

```bash
venv\Scripts\activate
```

Linux / Mac

```bash
source venv/bin/activate
```

Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔐 Environment Variables

Create `.env`

```env
DATABASE_URL=

SECRET_KEY=

MISTRAL_API_KEY=

MISTRAL_MODEL=

FRONTEND_URL=
```

---

# 🗄 Database Migration

```bash
alembic upgrade head
```

---

# ▶️ Run Server

```bash
uvicorn app.main:app --reload
```

Server

```
http://127.0.0.1:8000
```

Swagger Docs

```
/docs
```

---

# 👥 User Roles

### Customer

- Browse Restaurants
- AI Recommendations
- Add to Cart
- Checkout
- Reviews

### Restaurant Owner

- Create Restaurant
- Manage Menu
- Receive Orders
- Dashboard

### Admin

- Approve Restaurants
- Manage Users
- Analytics
- Platform Control

---

# 🚀 Deployment

Backend

- Railway

Database

- Neon PostgreSQL

Frontend

- Vercel

---

# 📈 Development Roadmap

## ✅ Phase 1

Authentication

## ✅ Phase 2

Restaurant & Menu

## ✅ Phase 3

Cart & Ordering

## ✅ Phase 4

AI Chat Assistant

## ✅ Phase 5

Analytics Dashboard

## 🔜 Phase 6

React Frontend

## 🔜 Phase 7

Payment Gateway

## 🔜 Phase 8

Real-Time Order Tracking

---

# 📚 API Documentation

Interactive API Documentation is available via Swagger.

```
/docs
```

---

# 🤝 Contributing

Contributions are welcome.

Fork the repository, create a feature branch, and submit a Pull Request.

---

# 📄 License

This project is licensed under the MIT License.
