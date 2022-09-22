from datetime import datetime
from typing import Optional, Tuple

from aiomysql import DictCursor
from configs import db_name_settings
from db import CreatePoolException, DBPoolManager
from py_singleton import singleton
from schemes.delivers import (
    DeliveryClub2Delivery,
    DeliveryClubDelivery,
    SushiDelivery,
    YandexDelivery,
)
from schemes.objects import ObjectCar, ObjectFio, ObservedObject


@singleton
class SearchService:
    async def search_by_phone(self, phone_number: str) -> ObservedObject:
        obj = await self.get_info_from_gibdd(ObservedObject(), phone_number)
        obj = await self.get_info_from_cdek(obj, phone_number)
        obj = await self.get_info_from_linkedin(obj, phone_number)
        obj = await self.get_info_from_pikabu(obj, phone_number)
        obj = await self.get_info_from_rfcont(obj, phone_number)
        obj = await self.get_info_from_vtb(obj, phone_number)
        obj = await self.get_info_from_wildberries(obj, phone_number)
        obj = await self.get_info_from_beeline(obj, phone_number)
        obj = await self.get_info_from_mailru(obj, phone_number)
        obj = await self.get_info_from_yandex(obj, phone_number)
        obj = await self.get_info_from_sushi(obj, phone_number)
        obj = await self.get_info_from_delivery_club1(obj, phone_number)
        obj = await self.get_info_from_delivery_club2(obj, phone_number)
        obj = await self.get_info_from_okrug(obj, phone_number)
        return obj

    async def get_info_from_gibdd(
        self, obj: ObservedObject, phone_number: str
    ) -> ObservedObject:
        data = await self._get_data_from_db(
            phone_number, db_name_settings.DB_GIBDD_NAME
        )

        if not data:
            return obj

        for car_data in data:
            car_scheme = ObjectCar(**car_data)
            obj.cars.append(car_scheme)

            fio = ObjectFio(full_name=car_scheme.owner_name)
            obj.fios.append(fio)

            if car_data.get("gibdd2_dateofbirth"):
                obj.birthdays.append(car_data.get("gibdd2_dateofbirth"))

        return obj

    async def get_info_from_yandex(
        self, obj: ObservedObject, phone_number: str
    ) -> ObservedObject:
        data = await self._get_data_from_db(
            phone_number, db_name_settings.DB_YANDEX_NAME
        )

        if not data:
            return obj

        for order_data in data:
            address_order = ", ".join(
                [
                    order_data.get("yandex_address_city"),
                    order_data.get("yandex_address_street"),
                    order_data.get("yandex_address_house"),
                ]
                + (
                    [order_data.get("yandex_address_office")]
                    if order_data.get("yandex_address_office")
                    else []
                )
            )

            yandex_order = YandexDelivery(
                customer_name=order_data.get("yandex_name"),
                date=order_data.get("yandex_created_at"),
                restaurant=(
                    order_data.get("yandex_place_name")
                    if order_data.get("yandex_place_name")
                    else str(order_data.get("yandex_place_id"))
                ),
                comment=order_data.get("yandex_address_comment"),
                order_sum=order_data.get("yandex_amount_rub"),
                orders_sum=order_data.get("yandex_sum_orders"),
                address=address_order,
            )
            obj.yandex_delivery_orders.append(yandex_order)

            fio = ObjectFio(full_name=yandex_order.customer_name)
            obj.fios.append(fio)

        return obj

    async def get_info_from_sushi(
        self, obj: ObservedObject, phone_number: str
    ) -> ObservedObject:
        data = await self._get_data_from_db(
            phone_number, db_name_settings.DB_SUSHI_NAME
        )

        if not data:
            return obj

        for order_data in data:
            address_order = ", ".join(
                [
                    order_data.get("sushi_address_city"),
                    order_data.get("sushi_address_street"),
                    order_data.get("sushi_address_home"),
                ]
                + (
                    [order_data.get("sushi_address_apartment")]
                    if order_data.get("sushi_address_apartment")
                    else []
                )
            )
            sushi_order = SushiDelivery(
                customer_name=order_data.get("sushi_name"),
                date=order_data.get("sushi_date"),
                restaurant="sushi",
                order_sum=order_data.get("sushi_amount_rub"),
                orders_sum=order_data.get("sushi_total_rub"),
                address=address_order,
            )
            obj.sushi_delivery_orders.append(sushi_order)

            fio = ObjectFio(full_name=sushi_order.customer_name)
            obj.fios.append(fio)

        return obj

    async def get_info_from_delivery_club1(
        self, obj: ObservedObject, phone_number: str
    ) -> ObservedObject:
        data = await self._get_data_from_db(
            phone_number, db_name_settings.DB_DELIVERY_NAME
        )

        if not data:
            return obj

        for order_data in data:
            order_scheme = DeliveryClubDelivery(**order_data)
            obj.delivery_club_delivery_orders.append(order_scheme)

            fio = ObjectFio(full_name=order_scheme.customer_name)
            obj.fios.append(fio)

        return obj

    async def get_info_from_delivery_club2(
        self, obj: ObservedObject, phone_number: str
    ) -> ObservedObject:
        data = await self._get_data_from_db(
            phone_number, db_name_settings.DB_DELIVERY_NAME
        )

        if not data:
            return obj

        for order_data in data:
            order_scheme = DeliveryClub2Delivery(**order_data)
            obj.delivery_club_delivery_orders.append(order_scheme)

            fio = ObjectFio(full_name=order_scheme.customer_name)
            obj.fios.append(fio)

            if order_data.get("delivery2_email"):
                obj.emails.append(order_data.get("delivery2_email"))

        return obj

    async def get_info_from_cdek(
        self, obj: ObservedObject, phone_number: str
    ) -> ObservedObject:
        data = await self._get_data_from_db(phone_number, db_name_settings.DB_CDEK_NAME)

        if not data:
            return obj

        for obj_data in data:
            if obj_data.get("cdek_full_name"):
                fio = ObjectFio(full_name=obj_data.get("cdek_full_name"))
                obj.fios.append(fio)
            if obj_data.get("cdek_email"):
                obj.emails.append(obj_data.get("cdek_email"))

        return obj

    async def get_info_from_pikabu(
        self, obj: ObservedObject, phone_number: str
    ) -> ObservedObject:
        data = await self._get_data_from_db(
            phone_number, db_name_settings.DB_PIKABU_NAME
        )

        if not data:
            return obj

        for obj_data in data:
            obj.pikabu_username = obj_data.get("pikabu_username")
            if obj_data.get("pikabu_email"):
                obj.emails.append(obj_data.get("pikabu_email"))

        return obj

    async def get_info_from_linkedin(
        self, obj: ObservedObject, phone_number: str
    ) -> ObservedObject:
        data = await self._get_data_from_db(
            phone_number, db_name_settings.DB_LINKEDIN_NAME
        )

        if not data:
            return obj

        for obj_data in data:
            if obj_data.get("linkedin_name"):
                fio = ObjectFio(full_name=obj_data.get("linkedin_name"))
                obj.fios.append(fio)
            if obj_data.get("linkedin_email"):
                obj.emails.append(obj_data.get("linkedin_email"))
            if obj_data.get("linkedin_link"):
                obj.linkedin_link = obj_data.get("linkedin_link")

        return obj

    async def get_info_from_rfcont(
        self, obj: ObservedObject, phone_number: str
    ) -> ObservedObject:
        data = await self._get_data_from_db(
            phone_number, db_name_settings.DB_RFCONT_NAME
        )

        if not data:
            return obj

        for obj_data in data:
            if obj_data.get("rfcont_name"):
                fio = ObjectFio(full_name=obj_data.get("rfcont_name"))
                obj.fios.append(fio)
            if obj_data.get("rfcont_email"):
                obj.emails.append(obj_data.get("rfcont_email"))

        return obj

    async def get_info_from_vtb(
        self, obj: ObservedObject, phone_number: str
    ) -> ObservedObject:
        data = await self._get_data_from_db(phone_number, db_name_settings.DB_VTB_NAME)

        if not data:
            return obj

        if data:
            obj.is_vtb = True

        return obj

    async def get_info_from_wildberries(
        self, obj: ObservedObject, phone_number: str
    ) -> ObservedObject:
        data = await self._get_data_from_db(
            phone_number, db_name_settings.DB_WILDBERRIES_NAME
        )

        if not data:
            return obj

        for obj_data in data:
            if obj_data.get("wildberries_name"):
                fio = ObjectFio(full_name=obj_data.get("wildberries_name"))
                obj.fios.append(fio)
            if obj_data.get("wildberries_email"):
                obj.emails.append(obj_data.get("wildberries_email"))
            if obj_data.get("wildberries_address"):
                obj.wildberries_addresses.append(obj_data.get("wildberries_address"))

        return obj

    async def get_info_from_beeline(
        self, obj: ObservedObject, phone_number: str
    ) -> ObservedObject:
        data = await self._get_data_from_db(
            phone_number, db_name_settings.DB_BEELINE_NAME
        )

        if not data:
            return obj

        for obj_data in data:
            if obj_data.get("beeline_full_name"):
                fio = ObjectFio(full_name=obj_data.get("beeline_full_name"))
                obj.fios.append(fio)

            address = (
                obj_data.get("beeline_address_city", "")
                + " "
                + obj_data.get("beeline_address_street", "")
                + " "
                + obj_data.get("beeline_address_house", "")
            )
            obj.addresses.append(address)

            if obj_data.get("beeline_inet_info"):
                obj.beeline_tariff = obj_data.get("beeline_inet_info")

        return obj

    async def get_info_from_mailru(
        self, obj: ObservedObject, phone_number: str
    ) -> ObservedObject:
        data = await self._get_data_from_db(
            phone_number, db_name_settings.DB_MAILRU_NAME
        )

        if not data:
            return obj

        for obj_data in data:
            if obj_data.get("mailru_full_name"):
                fio = ObjectFio(full_name=obj_data.get("mailru_full_name"))
                obj.fios.append(fio)

            obj.emails.append(obj_data.get("mailru_email"))

            if obj_data.get("mailru_education"):
                obj.educations = obj_data.get("mailru_education")

        return obj

    async def get_info_from_okrug(
        self, obj: ObservedObject, phone_number: str
    ) -> ObservedObject:
        data = await self._get_data_from_db(
            phone_number, db_name_settings.DB_OKRUG_NAME
        )

        if not data:
            return obj

        for obj_data in data:
            if obj_data.get("okrug_pib"):
                fio = ObjectFio(full_name=obj_data.get("okrug_pib"))
                obj.fios.append(fio)

            if obj_data.get("okrug_birth"):
                obj.birthdays.append(
                    datetime.strptime(obj_data.get("okrug_birth"), "%m/%d/%Y").date()
                )

        return obj

    async def _get_data_from_db(
        self, phone_number: str, db_name: Optional[str]
    ) -> Optional[Tuple]:
        if not db_name:
            return None

        return await self._search_in_db(phone_number, db_name)

    @staticmethod
    async def _search_in_db(phone_number: str, db_name: str) -> Tuple:
        try:
            pool = await DBPoolManager().get_connect(db_name)
        except CreatePoolException:
            print(f"Error: no connect to db: {db_name}")
            return ()

        async with pool.acquire() as connect:
            async with connect.cursor(DictCursor) as cursor:
                await cursor.execute(
                    f"SELECT * FROM {db_name.lower()}_full WHERE phone_number = '{phone_number}'"
                )
                result = cursor.fetchall()

        return result.result()
