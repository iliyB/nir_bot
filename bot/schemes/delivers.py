from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class DeliveryBaseScheme(BaseModel):
    customer_name: Optional[str] = None
    date: Optional[datetime] = None
    address: Optional[str] = None
    comment: Optional[str] = None
    order_sum: Optional[float] = None
    orders_sum: Optional[float] = None
    restaurant: Optional[str] = None


class YandexDelivery(DeliveryBaseScheme):
    pass


class DeliveryClubDelivery(DeliveryBaseScheme):
    customer_name: Optional[str] = Field(None, alias="delivery_name")
    date: Optional[datetime] = Field(None, alias="delivery_created")
    address: Optional[str] = Field(None, alias="delivery_address")
    comment: Optional[str] = Field(None, alias="delivery_comment")
    order_sum: Optional[float] = Field(None, alias="delivery_amount_rub")
    orders_sum: Optional[float] = Field(None, alias="delivery_total_rub")


class DeliveryClub2Delivery(DeliveryBaseScheme):
    customer_name: Optional[str] = Field(None, alias="delivery2_name")
    date: Optional[datetime] = Field(None, alias="delivery2_created_at")
    city: Optional[str] = Field(None, alias="delivery2_address_city")
    address: Optional[str] = Field(None, alias="delivery2_address_full")
    street: Optional[str] = Field(None, alias="delivery2_address_street")
    building: Optional[str] = Field(None, alias="delivery2_address_building")
    flat: Optional[str] = Field(None, alias="delivery2_address_flat_number")
    comment: Optional[str] = Field(None, alias="delivery2_address_instructions")
    order_sum: Optional[float] = Field(None, alias="delivery2_price_client_rub")
    orders_sum: Optional[float] = Field(None, alias="delivery2_pricetotal_rub")
    restaurant: Optional[str] = Field(None, alias="delivery2_vendor_name")


class SushiDelivery(DeliveryBaseScheme):
    pass
