from decimal import Decimal

from pydantic import BaseModel


class TopSellingItem(BaseModel):
    food_name: str
    total_quantity: int


class RestaurantDashboardOut(BaseModel):
    total_orders: int
    total_revenue: Decimal
    orders_by_status: dict[str, int]
    top_selling_items: list[TopSellingItem]
