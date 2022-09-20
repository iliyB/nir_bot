from typing import Optional

from pydantic import BaseModel


class DeliveryMixin(BaseModel):
    order_id: Optional[int] = None
    customer_name: Optional[str] = None
    address: Optional[str] = None
    comment: Optional[str] = None
    order_sum: Optional[float] = None
    orders_sum: Optional[float] = None


class YandexDelivery(DeliveryMixin):
    pass


class TwoBeregaDelivery(DeliveryMixin):
    pass


class DeliveryClubDelivery(DeliveryMixin):
    about_order: Optional[str] = None
    restaurant: Optional[str] = None


class SushiDelivery(DeliveryMixin):
    restaurant: Optional[str] = None
