from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import (
    auth_routes,
    category_routes,
    restaurant_routes,
    food_routes,
    cart_routes,
    order_routes,
    chat_routes,
    review_routes,
    admin_routes,
    dashboard_routes,
)
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

# CORS - allow frontend (React) to talk to backend.
# Local dev (Vite) is always allowed; production frontend URL comes from .env (FRONTEND_URL),
# so no code change is needed when deploying — just set the env var on Railway.
allowed_origins = list({"http://localhost:5173", settings.FRONTEND_URL})

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes.router)
app.include_router(category_routes.router)
app.include_router(restaurant_routes.router)
app.include_router(food_routes.router)
app.include_router(cart_routes.router)
app.include_router(order_routes.router)
app.include_router(chat_routes.router)
app.include_router(review_routes.router)
app.include_router(admin_routes.router)
app.include_router(dashboard_routes.router)


@app.get("/")
def root():
    return {"message": f"{settings.PROJECT_NAME} API is running", "status": "ok"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
