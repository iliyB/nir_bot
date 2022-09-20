from datetime import date
from typing import List, Optional

from pydantic import BaseModel, Field

from nir_bot.bot.schemes.delivers import (
    DeliveryClubDelivery,
    SushiDelivery,
    TwoBeregaDelivery,
    YandexDelivery,
)


class ObjectFio(BaseModel):
    first_name: Optional[str] = []
    last_name: Optional[str] = None
    middle_name: Optional[str] = None

    full_name: Optional[str] = None


class ObjectCar(BaseModel):
    number: Optional[str] = None
    old_number: Optional[str] = None

    model: Optional[str] = None
    color: Optional[str] = None
    release_date: Optional[int] = Field(None, gt=1900, lt=2100)

    win: Optional[int] = None
    owner_name: Optional[str] = None
    owner_birthday: Optional[str] = None

    place_if_driver_license: Optional[str] = None


class ObservedObject(BaseModel):
    fios: List[ObjectFio] = []

    emails: List[str] = []
    addresses: List[str] = []

    birthdays: List[date] = []
    cars: List[ObjectCar] = []

    yandex_delivery_orders: List[YandexDelivery] = []
    two_berega_delivery_orders: List[TwoBeregaDelivery] = []
    delivery_club_delivery_orders: List[DeliveryClubDelivery] = []
    sushi_delivery_orders: List[SushiDelivery] = []

    pikabu_usernames: Optional[str] = None
