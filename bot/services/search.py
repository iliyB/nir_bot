import re
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
from schemes.objects import ObjectCar, ObservedObject


@singleton
class SearchService:
    async def search_in_db(
        self, search_value: str, obj: Optional[ObservedObject] = None
    ) -> ObservedObject:
        if not obj:
            obj = ObservedObject()

        obj = await self.get_info_from_gibdd(obj, search_value)
        obj = await self.get_info_from_cdek(obj, search_value)
        obj = await self.get_info_from_linkedin(obj, search_value)
        obj = await self.get_info_from_pikabu(obj, search_value)
        obj = await self.get_info_from_rfcont(obj, search_value)
        obj = await self.get_info_from_vtb(obj, search_value)
        obj = await self.get_info_from_wildberries(obj, search_value)
        obj = await self.get_info_from_beeline(obj, search_value)
        obj = await self.get_info_from_mailru(obj, search_value)
        obj = await self.get_info_from_yandex(obj, search_value)
        obj = await self.get_info_from_sushi(obj, search_value)
        obj = await self.get_info_from_delivery_club1(obj, search_value)
        obj = await self.get_info_from_delivery_club2(obj, search_value)
        obj = await self.get_info_from_okrug(obj, search_value)

        if "@" in search_value and search_value not in obj.emails:
            obj.emails.append(search_value)
        elif "@" not in search_value and search_value not in obj.phones:
            obj.phones.append(str(search_value))

        obj.searched_by.add(search_value)

        return obj

    async def get_info_from_gibdd(
        self, obj: ObservedObject, search_value: str
    ) -> ObservedObject:
        data = await self._get_data_from_db(
            search_value, db_name_settings.DB_GIBDD_NAME
        )

        if not data:
            return obj

        for car_data in data:
            car_scheme = ObjectCar(**car_data)
            obj.cars.append(car_scheme)

            obj.fios.append(car_scheme.owner_name)

            if car_data.get("gibdd2_dateofbirth"):
                obj.birthdays.append(car_data.get("gibdd2_dateofbirth"))

        return obj

    async def get_info_from_yandex(
        self, obj: ObservedObject, search_value: str
    ) -> ObservedObject:
        data = await self._get_data_from_db(
            search_value, db_name_settings.DB_YANDEX_NAME
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

            obj.fios.append(yandex_order.customer_name)
            obj.addresses.append(address_order)

            obj.addresses_analyze[address_order] = [float(order_data.get("yandex_longitude")), float(order_data.get("yandex_latitude"))]
            obj.order_addresses_full.append(address_order)
        return obj

    async def get_info_from_sushi(
        self, obj: ObservedObject, search_value: str
    ) -> ObservedObject:
        data = await self._get_data_from_db(
            search_value, db_name_settings.DB_SUSHI_NAME
        )

        if not data:
            return obj

        for order_data in data:

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

            obj.fios.append(sushi_order.customer_name)
            obj.addresses.append(address_order)
            obj.addresses_analyze[address_order] = [float(order_data.get("sushi_long")), float(order_data.get("sushi_lat"))]
            obj.order_addresses_full.append(address_order)
        return obj

    async def get_info_from_delivery_club1(
        self, obj: ObservedObject, search_value: str
    ) -> ObservedObject:
        data = await self._get_data_from_db(
            search_value, db_name_settings.DB_DELIVERY_NAME
        )

        if not data:
            return obj

        for order_data in data:
            order_scheme = DeliveryClubDelivery(**order_data)
            obj.delivery_club_delivery_orders.append(order_scheme)

            obj.fios.append(order_scheme.customer_name)
            obj.addresses.append(order_scheme.address)
            obj.addresses_analyze[order_scheme.address] = [float(order_data.get("delivery_long")), float(order_data.get("delivery_lat"))]
            obj.order_addresses_full.append(order_scheme.address)
        return obj

    async def get_info_from_delivery_club2(
        self, obj: ObservedObject, search_value: str
    ) -> ObservedObject:
        data = await self._get_data_from_db(
            search_value, db_name_settings.DB_DELIVERY2_NAME
        )

        if not data:
            return obj

        for order_data in data:
            order_scheme = DeliveryClub2Delivery(**order_data)
            obj.delivery_club_delivery_orders.append(order_scheme)

            obj.fios.append(order_scheme.customer_name)
            address_order = order_scheme.city + ', улица ' + order_scheme.street + ', дом ' + order_scheme.building + ', кв/офис ' + order_scheme.flat
            obj.addresses.append(address_order)
            obj.order_addresses_full.append(address_order)
            obj.addresses_analyze[address_order] = [float(order_data.get("delivery2_longitude")), float(order_data.get("delivery2_latitude"))]

            if "@" in search_value and order_data.get("phone_number"):
                obj.phones.append(str(order_data.get("phone_number")))
            elif order_data.get("delivery2_email"):
                obj.emails.append(order_data.get("delivery2_email"))

        return obj

    async def get_info_from_cdek(
        self, obj: ObservedObject, search_value: str
    ) -> ObservedObject:
        data = await self._get_data_from_db(search_value, db_name_settings.DB_CDEK_NAME)

        if not data:
            return obj

        for obj_data in data:
            if obj_data.get("cdek_full_name"):
                obj.fios.append(obj_data.get("cdek_full_name"))

            if "@" in search_value and obj_data.get("phone_number"):
                obj.phones.append(str(obj_data.get("phone_number")))
            elif obj_data.get("cdek_email"):
                obj.emails.append(obj_data.get("cdek_email"))

        return obj

    async def get_info_from_pikabu(
        self, obj: ObservedObject, search_value: str
    ) -> ObservedObject:
        data = await self._get_data_from_db(
            search_value, db_name_settings.DB_PIKABU_NAME
        )

        if not data:
            return obj

        for obj_data in data:
            obj.pikabu_username = obj_data.get("pikabu_username")

            if "@" in search_value and obj_data.get("phone_number"):
                obj.phones.append(str(obj_data.get("phone_number")))
            elif obj_data.get("pikabu_email"):
                obj.emails.append(obj_data.get("pikabu_email"))

        return obj

    async def get_info_from_linkedin(
        self, obj: ObservedObject, search_value: str
    ) -> ObservedObject:
        data = await self._get_data_from_db(
            search_value, db_name_settings.DB_LINKEDIN_NAME
        )

        if not data:
            return obj

        for obj_data in data:
            if obj_data.get("linkedin_name"):
                obj.fios.append(obj_data.get("linkedin_name"))

            if "@" in search_value and obj_data.get("phone_number"):
                obj.phones.append(str(obj_data.get("phone_number")))
            elif obj_data.get("linkedin_email"):
                obj.emails.append(obj_data.get("linkedin_email"))

            if obj_data.get("linkedin_link"):
                obj.linkedin_link = obj_data.get("linkedin_link")

        return obj

    async def get_info_from_rfcont(
        self, obj: ObservedObject, search_value: str
    ) -> ObservedObject:
        data = await self._get_data_from_db(
            search_value, db_name_settings.DB_RFCONT_NAME
        )

        if not data:
            return obj

        for obj_data in data:
            if obj_data.get("rfcont_name"):
                obj.fios.append(obj_data.get("rfcont_name"))

            if "@" in search_value and obj_data.get("phone_number"):
                obj.phones.append(str(obj_data.get("phone_number")))
            elif obj_data.get("rfcont_email"):
                obj.emails.append(obj_data.get("rfcont_email"))

        return obj

    async def get_info_from_vtb(
        self, obj: ObservedObject, search_value: str
    ) -> ObservedObject:
        data = await self._get_data_from_db(search_value, db_name_settings.DB_VTB_NAME)

        if not data:
            return obj

        if data:
            obj.is_vtb = True

        return obj

    async def get_info_from_wildberries(
        self, obj: ObservedObject, search_value: str
    ) -> ObservedObject:
        data = await self._get_data_from_db(
            search_value, db_name_settings.DB_WILDBERRIES_NAME
        )

        if not data:
            return obj

        for obj_data in data:
            if obj_data.get("wildberries_name"):
                obj.fios.append(obj_data.get("wildberries_name"))

            if "@" in search_value and obj_data.get("phone_number"):
                obj.phones.append(str(obj_data.get("phone_number")))
            elif obj_data.get("wildberries_email"):
                obj.emails.append(obj_data.get("wildberries_email"))

            if obj_data.get("wildberries_address"):
                obj.wildberries_addresses.append(obj_data.get("wildberries_address"))

        return obj

    async def get_info_from_beeline(
        self, obj: ObservedObject, search_value: str
    ) -> ObservedObject:
        data = await self._get_data_from_db(
            search_value, db_name_settings.DB_BEELINE_NAME
        )

        if not data:
            return obj

        for obj_data in data:
            if obj_data.get("beeline_full_name"):
                obj.fios.append(obj_data.get("beeline_full_name"))

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
        self, obj: ObservedObject, search_value: str
    ) -> ObservedObject:
        data = await self._get_data_from_db(
            search_value, db_name_settings.DB_MAILRU_NAME
        )

        if not data:
            return obj

        for obj_data in data:
            if obj_data.get("mailru_full_name"):
                obj.fios.append(obj_data.get("mailru_full_name"))

            if "@" in search_value and obj_data.get("phone_number"):
                obj.phones.append(str(obj_data.get("phone_number")))
            elif obj_data.get("mailru_email"):
                obj.emails.append(obj_data.get("mailru_email"))

           # if obj_data.get("mailru_education"):
             #   obj.educations = obj_data.get("mailru_education")

        return obj

    async def get_info_from_okrug(
        self, obj: ObservedObject, search_value: str
    ) -> ObservedObject:
        data = await self._get_data_from_db(
            search_value, db_name_settings.DB_OKRUG_NAME
        )

        if not data:
            return obj

        for obj_data in data:
            if obj_data.get("okrug_pib"):
                obj.fios.append(obj_data.get("okrug_pib"))

            if obj_data.get("okrug_birth"):
                obj.birthdays.append(
                    datetime.strptime(obj_data.get("okrug_birth"), "%m/%d/%Y").date()
                )

        return obj

    async def _get_data_from_db(
        self, search_value: str, db_name: Optional[str]
    ) -> Optional[Tuple]:
        if not db_name:
            return None

        if "@" in search_value:
            return await self._search_by_email_in_db(search_value, db_name)
        else:
            return await self._search_by_phone_in_db(search_value, db_name)

    @staticmethod
    async def _search_by_phone_in_db(phone_number: str, db_name: str) -> Tuple:
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

    @staticmethod
    async def _search_by_email_in_db(email: str, db_name: str) -> Tuple:
        try:
            pool = await DBPoolManager().get_connect(db_name)
        except CreatePoolException:
            print(f"Error: no connect to db: {db_name}")
            return ()

        try:
            async with pool.acquire() as connect:
                async with connect.cursor(DictCursor) as cursor:
                    await cursor.execute(
                        f"SELECT * FROM {db_name.lower()}_full WHERE {db_name.lower()}_email = '{email}'"
                    )
                    result = cursor.fetchall()
        except:
            return tuple()

        return result.result()
