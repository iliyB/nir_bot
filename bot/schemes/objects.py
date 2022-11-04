from datetime import date
from typing import List, Optional

from pydantic import BaseModel, Field
from schemes.delivers import DeliveryBaseScheme


class ObjectFio(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    middle_name: Optional[str] = None

    full_name: Optional[str] = None


class ObjectCar(BaseModel):
    number: Optional[str] = Field(None, alias="gibdd2_car_plate_number")
    old_number: Optional[str] = Field(None, alias="gibdd2_old_car_plate_numberr")

    model: Optional[str] = Field(None, alias="gibdd2_car_model")
    color: Optional[str] = Field(None, alias="gibdd2_car_color")
    release_year: Optional[int] = Field(None, gt=0, lt=2100, alias="gibdd2_car_year")

    vin: Optional[str] = Field(None, alias="gibdd2_car_vin")
    owner_name: Optional[str] = Field(None, alias="gibdd2_base_name")
    owner_birthday: Optional[date] = Field(None, alias="gibdd2_dateofbirth")

    place_if_driver_license: Optional[str] = Field(None, alias="gibdd2_passport")


class ObservedObject(BaseModel):
    fios: List[ObjectFio] = []

    emails: List[str] = []
    addresses: List[str] = []

    birthdays: List[date] = []
    cars: List[ObjectCar] = []

    yandex_delivery_orders: List[DeliveryBaseScheme] = []
    two_berega_delivery_orders: List[DeliveryBaseScheme] = []
    delivery_club_delivery_orders: List[DeliveryBaseScheme] = []
    sushi_delivery_orders: List[DeliveryBaseScheme] = []

    wildberries_addresses: List[str] = []

    linkedin_link: Optional[str] = None
    pikabu_username: Optional[str] = None
    is_vtb: bool = False
    beeline_tariff: Optional[str] = None
    educations: List[str] = []
