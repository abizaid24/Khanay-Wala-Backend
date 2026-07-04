# KhanayWala Backend — Phase 1: Foundation & Authentication

Ye Phase 1 hai: project setup, database connection, aur JWT-based authentication system
(Register, Login, Refresh Token, Profile) — Customer / Restaurant Owner / Admin roles ke sath.

## Setup (local machine pe)

1. **Virtual environment banao:**
   ```bash
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   ```

2. **Dependencies install karo:**
   ```bash
   pip install -r requirements.txt
   ```

3. **PostgreSQL database banao** (local ya Railway pe), phir `.env.example` ko `.env` mein copy karo aur values fill karo:
   ```bash
   cp .env.example .env
   ```
   - `DATABASE_URL` apne Postgres connection string se replace karo
   - `SECRET_KEY` ek strong random string se replace karo (e.g. `openssl rand -hex 32`)

4. **Migration generate aur apply karo** (users table banane ke liye):
   ```bash
   alembic revision --autogenerate -m "create users table"
   alembic upgrade head
   ```

5. **Server run karo:**
   ```bash
   uvicorn app.main:app --reload
   ```
   Server `http://127.0.0.1:8000` pe chalega. Interactive API docs: `http://127.0.0.1:8000/docs`

## Phase 1 Endpoints

| Method | Endpoint             | Description                          | Auth Required |
|--------|-----------------------|---------------------------------------|----------------|
| POST   | `/api/auth/register`  | Naya user register karo (customer/owner/admin) | No |
| POST   | `/api/auth/login`     | Login (email + password), access + refresh token milega | No |
| POST   | `/api/auth/refresh`   | Refresh token se naya access token lo | No (refresh token needed) |
| GET    | `/api/auth/profile`   | Apna profile dekho                    | Yes (Bearer token) |

## Test karne ka tarika (Swagger UI se)

1. `/docs` kholo
2. `/api/auth/register` try karo — full_name, email, password, role (`customer`/`restaurant_owner`/`admin`) do
3. `/api/auth/login` try karo — username field mein email daalo, password daalo
4. Response se `access_token` copy karo
5. Top-right "Authorize" button pe click karo, token paste karo
6. `/api/auth/profile` call karo — apna data wapis milega

## Folder Structure (Phase 1)

```
app/
 ├── api/            → route handlers (auth_routes.py)
 ├── auth/           → security.py (JWT + hashing), dependencies.py (route protection)
 ├── core/           → config.py (settings from .env)
 ├── crud/           → database operations (user.py)
 ├── db/             → database.py (engine, session)
 ├── models/         → SQLAlchemy models (user.py)
 ├── schemas/        → Pydantic schemas (user.py)
 ├── migrations/     → Alembic migration files
 └── main.py         → FastAPI app entrypoint
```

---

# Phase 2: Restaurant & Menu System

Is phase mein add hua: Categories (admin managed), Restaurants (owner creates, admin approves),
aur Food Items / Menu (owner manages, sab public browse kar sakte hain).

## Naye Models
- **Category** — global food categories (e.g. Fast Food, BBQ, Chinese) — sirf admin add/delete kar sakta hai
- **Restaurant** — restaurant_owner create karta hai; admin approve karta hai (`is_approved`); customers ko sirf approved + active restaurants dikhte hain
- **FoodItem** — restaurant ka menu item, price/category/image ke sath

## Migration chalao (naye tables ke liye)

```bash
alembic revision --autogenerate -m "add categories, restaurants, food_items tables"
alembic upgrade head
```

## Phase 2 Endpoints

**Categories**
| Method | Endpoint | Description | Auth |
|--------|----------|--------------|------|
| GET | `/api/categories` | Sab categories list | Public |
| POST | `/api/categories` | Naya category banao | Admin |
| DELETE | `/api/categories/{id}` | Category delete karo | Admin |

**Restaurants**
| Method | Endpoint | Description | Auth |
|--------|----------|--------------|------|
| POST | `/api/restaurants` | Apna restaurant create karo | Restaurant Owner |
| GET | `/api/restaurants?search=` | Browse/search approved restaurants | Public |
| GET | `/api/restaurants/mine` | Apne sab restaurants dekho | Restaurant Owner |
| GET | `/api/restaurants/pending` | Approval ke liye pending restaurants | Admin |
| GET | `/api/restaurants/{id}` | Ek restaurant ki detail | Public |
| PUT | `/api/restaurants/{id}` | Restaurant update karo | Owner / Admin |
| PATCH | `/api/restaurants/{id}/approve` | Restaurant approve karo | Admin |

**Menu / Food Items**
| Method | Endpoint | Description | Auth |
|--------|----------|--------------|------|
| POST | `/api/restaurants/{restaurant_id}/foods` | Menu item add karo | Owner (apna restaurant) |
| GET | `/api/restaurants/{restaurant_id}/foods` | Restaurant ka pura menu dekho | Public |
| GET | `/api/foods/search?q=` | Food items search karo (sab restaurants mein) | Public |
| PUT | `/api/foods/{food_id}` | Menu item update karo | Owner / Admin |
| DELETE | `/api/foods/{food_id}` | Menu item delete karo | Owner / Admin |

## Test flow (Swagger `/docs` pe)

1. Ek `admin` role wala user register/login karo → `/api/categories` POST se 2-3 categories add karo
2. Ek `restaurant_owner` register/login karo → `/api/restaurants` POST se restaurant banao
3. Admin token se `/api/restaurants/pending` dekho, phir `/api/restaurants/{id}/approve` call karo
4. Owner token se `/api/restaurants/{restaurant_id}/foods` POST se menu items add karo
5. Bina login kiye `/api/restaurants` aur `/api/restaurants/{id}/foods` try karo — public visible hone chahiye

---

# Phase 3: Cart & Ordering Flow

Is phase mein add hua: Cart (per customer), Cart Items, Orders, Order Items, aur order status
tracking (pending → preparing → out_for_delivery → delivered, ya cancelled).

## Naye Models
- **Cart / CartItem** — har customer ka ek active cart hota hai. **Important rule:** cart mein sirf
  ek restaurant ke items ho sakte hain (jaisay real Foodpanda/Zomato mein hota hai) — doosray
  restaurant ka item add karne ki koshish karo ge to error milega jab tak cart clear na karo
- **Order / OrderItem** — checkout par cart se order banta hai. Food ka naam aur price **snapshot**
  ho jata hai order mein (agar baad mein owner price change kare, purane orders affect nahi honge)
- **Order status transitions controlled hain** — sirf sahi sequence mein status change ho sakta hai
  (e.g. `pending` seedha `delivered` nahi ban sakta, pehle `preparing` se guzarna hoga)

## Migration chalao

```bash
alembic revision --autogenerate -m "add cart, cart_items, orders, order_items tables"
alembic upgrade head
```

## Phase 3 Endpoints

**Cart** (Customer only)
| Method | Endpoint | Description |
|--------|----------|--------------|
| GET | `/api/cart` | Apna cart dekho (khali ho to auto-create hoga) |
| POST | `/api/cart/items` | Item add karo `{food_item_id, quantity}` |
| PUT | `/api/cart/items/{item_id}` | Quantity update karo |
| DELETE | `/api/cart/items/{item_id}` | Ek item remove karo |
| DELETE | `/api/cart` | Pura cart khali karo |

**Orders**
| Method | Endpoint | Description | Auth |
|--------|----------|--------------|------|
| POST | `/api/orders/checkout` | Cart se order place karo `{delivery_address, notes}` | Customer |
| GET | `/api/orders` | Apni order history dekho | Customer |
| GET | `/api/orders/{order_id}` | Order detail dekho | Customer (owner) / Restaurant Owner / Admin |
| GET | `/api/orders/restaurant/{restaurant_id}` | Restaurant ke incoming orders | Restaurant Owner / Admin |
| PATCH | `/api/orders/{order_id}/status` | Order status update karo | Restaurant Owner / Admin |

## Test flow (Swagger `/docs` pe)

1. Customer login karo → `/api/cart/items` se Phase 2 wale menu items add karo
2. `/api/cart` se dekho total sahi calculate ho raha hai
3. `/api/orders/checkout` call karo, delivery address do → order ban jaye ga, cart khali ho jaye ga
4. Restaurant owner login karke `/api/orders/restaurant/{restaurant_id}` se order dekho
5. `/api/orders/{order_id}/status` se status `preparing` → `out_for_delivery` → `delivered` karo
6. Galat sequence try karo (e.g. `pending` se `delivered`) — error milna chahiye

---

# Phase 4: AI Chat Assistant & Reviews

Is phase mein add hua: **Mistral AI** se powered Chat Assistant (chat history ke sath),
aur ek **verified-purchase Reviews system**.

> **Note:** Project doc mein originally Google Gemini likha tha, lekin AI provider **Mistral AI**
> use kiya gaya hai (jo key tumne di thi). Service layer `app/ai/mistral_client.py` mein isolated
> hai — agar kabhi Gemini pe switch karna ho to sirf ye ek file badalni hogi, baaki code same rahega.

## Naye Models
- **AIChatHistory** — customer ke messages aur AI ke replies save hote hain (last 5 turns AI ko
  context ke taur pe bheje jate hain, taake conversation yaad rahe)
- **Review** — sirf **delivered order** pe review ho sakta hai (verified purchase), aur ek order
  pe sirf ek hi review ban sakta hai

## Migration chalao

```bash
alembic revision --autogenerate -m "add ai_chat_history and reviews tables"
alembic upgrade head
```

## Phase 4 Endpoints

**AI Chat Assistant** (Customer only)
| Method | Endpoint | Description |
|--------|----------|--------------|
| POST | `/api/chat` | AI se baat karo `{message}` → AI ka reply milta hai |
| GET | `/api/chat/history` | Apni purani chat history dekho |

**Reviews**
| Method | Endpoint | Description | Auth |
|--------|----------|--------------|------|
| POST | `/api/reviews` | Review do `{order_id, rating, comment}` | Customer (apna delivered order) |
| GET | `/api/restaurants/{restaurant_id}/reviews` | Restaurant ke sab reviews dekho | Public |
| DELETE | `/api/reviews/{review_id}` | Review delete karo | Review ka owner / Admin |

## Test flow (Swagger `/docs` pe)

1. Customer login karo → `/api/chat` pe koi message bhejo (e.g. "mujhe kuch spicy suggest karo") → AI ka reply aana chahiye
2. `/api/chat/history` se purani chat dekho
3. Phase 3 wale order ko owner se `delivered` status tak le jao
4. `/api/reviews` POST karo us order_id ke sath — review ban jaye ga
5. Wohi order dobara review karne ki koshish karo — error milna chahiye ("already reviewed")
6. Bina login `/api/restaurants/{id}/reviews` try karo — public visible hona chahiye

---

# Phase 5: Admin Dashboard, Analytics & Deployment

Ye backend ka **aakhri phase** hai: Admin panel (users/restaurants manage), owner ke liye Sales
Dashboard, platform-wide Analytics, aur Railway/Vercel pe deploy karne ki guide.

## Phase 5 Endpoints

**Admin** (sab `/api/admin/*` routes admin-only hain)
| Method | Endpoint | Description |
|--------|----------|--------------|
| GET | `/api/admin/users` | Sab users ki list (role, active status ke sath) |
| PATCH | `/api/admin/users/{user_id}/deactivate` | User ko deactivate karo (login nahi kar sakega) |
| PATCH | `/api/admin/users/{user_id}/activate` | User ko dobara activate karo |
| GET | `/api/admin/restaurants` | Sab restaurants — pending/approved/inactive sab |
| GET | `/api/admin/analytics` | Platform-wide stats: total users, restaurants, orders, revenue, status breakdown |

**Owner Sales Dashboard**
| Method | Endpoint | Description | Auth |
|--------|----------|--------------|------|
| GET | `/api/restaurants/{restaurant_id}/dashboard` | Apne restaurant ke orders, revenue, top-selling items | Owner / Admin |

## Test flow (Swagger `/docs` pe)

1. Admin login karo → `/api/admin/analytics` se overall platform stats dekho
2. `/api/admin/users` se list dekho, kisi user ko `/deactivate` karo, phir us user se login try karo — fail hona chahiye
3. Owner login karke `/api/restaurants/{restaurant_id}/dashboard` se apni sales dekho — total orders, revenue, top items

## Deployment Guide

### 1. Database — Neon PostgreSQL (already set up)
Tumhara `DATABASE_URL` already `.env` mein hai (Neon).

### 2. Backend — Railway
1. Ye poora `food-delivery-backend/` folder ek GitHub repo mein push karo (`.env` push mat karna — `.gitignore` already exclude karta hai)
2. Railway pe naya project banao → "Deploy from GitHub repo"
3. Railway project ke **Variables** tab mein ye sab env vars add karo (apni `.env` file se copy):
   - `DATABASE_URL`
   - `SECRET_KEY` (production ke liye naya strong random string banao)
   - `MISTRAL_API_KEY`
   - `MISTRAL_MODEL`
   - `FRONTEND_URL` (abhi ke liye `http://localhost:5173` rakho, Vercel deploy hone ke baad update karo)
4. Railway `Procfile` khud detect kar lega:
   - `release: alembic upgrade head` → deploy hote hi migrations apne aap chal jayengi
   - `web: uvicorn app.main:app --host 0.0.0.0 --port $PORT` → server start
5. Deploy hone ke baad Railway ek public URL de ga (e.g. `https://khanaywala-backend.up.railway.app`) — ye tumhara live backend URL hai

### 3. Frontend — Vercel
Frontend (React) abhi tak nahi bana — ye **Phase 6+ (frontend build)** mein hoga. Jab bane ga,
Vercel pe deploy hoga aur uska URL Railway ke `FRONTEND_URL` variable mein update karna hoga
(taake CORS sahi kaam kare).

## Backend Complete! 🎉

Poora backend (Phase 1–5) ab feature-complete hai:
- ✅ Auth (JWT, role-based)
- ✅ Restaurants & Menu
- ✅ Cart & Orders
- ✅ AI Chat Assistant (Mistral) & Reviews
- ✅ Admin Dashboard & Analytics
- ✅ Deployment-ready (Railway + Neon)

## Agla Kadam

Ab hum **Frontend (React + Vite + Tailwind + Shadcn UI)** shuru karenge, jo isi backend ke sath
connect hoga. Wahan bhi wahi approach rakhenge — ek phase mukammal karke test karo, phir agla.
