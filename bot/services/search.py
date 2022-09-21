from typing import Optional, Tuple

from aiomysql import DictCursor
from configs import db_name_settings
from db import CreatePoolException, DBPoolManager
from py_singleton import singleton
from schemes.objects import ObjectCar, ObjectFio, ObservedObject


@singleton
class SearchService:
    async def search_by_phone(self, phone_number: str) -> Optional[ObservedObject]:
        obj = await self.get_info_from_gibdd(ObservedObject(), phone_number)
        obj = await self.get_info_from_cdek(obj, phone_number)
        obj = await self.get_info_from_linkedin(obj, phone_number)
        obj = await self.get_info_from_pikabu(obj, phone_number)
        obj = await self.get_info_from_rfcont(obj, phone_number)
        obj = await self.get_info_from_vtb(obj, phone_number)
        obj = await self.get_info_from_wildberries(obj, phone_number)
        obj = await self.get_info_from_beeline(obj, phone_number)
        obj = await self.get_info_from_mailru(obj, phone_number)
        # await self.search_in_db(phone_number, db_connect_settings.DB_YANDEX_NAME)
        # await self.search_in_db(phone_number, db_connect_settings.DB_DELIVERY_NAME)
        # await self.search_in_db(phone_number, db_connect_settings.DB_DELIVERY2_NAME)
        # await self.search_in_db(phone_number, db_connect_settings.DB_SUSHI_NAME)
        return obj

    async def get_info_from_gibdd(
        self, obj: ObservedObject, phone_number: str
    ) -> ObservedObject:
        db_name = db_name_settings.DB_GIBDD_NAME
        if not db_name:
            return obj

        data = await self._search_in_db(phone_number, db_name)

        if not data:
            return obj

        for car_data in data:
            car_scheme = ObjectCar(**car_data)
            obj.cars.append(car_scheme)

            fio = ObjectFio(full_name=car_scheme.owner_name)
            obj.fios.append(fio)

            if car_data["gibdd2_dateofbirth"]:
                obj.birthdays.append(car_data["gibdd2_dateofbirth"])

        return obj

    async def get_info_from_cdek(
        self, obj: ObservedObject, phone_number: str
    ) -> ObservedObject:
        db_name = db_name_settings.DB_CDEK_NAME
        if not db_name:
            return obj

        data = await self._search_in_db(phone_number, db_name)

        if not data:
            return obj

        for obj_data in data:
            if obj_data["cdek_full_name"]:
                fio = ObjectFio(full_name=obj_data["cdek_full_name"])
                obj.fios.append(fio)
            if obj_data["cdek_email"]:
                obj.emails.append(obj_data["cdek_email"])

        return obj

    async def get_info_from_pikabu(
        self, obj: ObservedObject, phone_number: str
    ) -> ObservedObject:
        db_name = db_name_settings.DB_PIKABU_NAME
        if not db_name:
            return obj

        data = await self._search_in_db(phone_number, db_name)

        if not data:
            return obj

        for obj_data in data:
            obj.pikabu_username = obj_data["pikabu_username"]
            if obj_data["pikabu_email"]:
                obj.emails.append(obj_data["pikabu_email"])

        return obj

    async def get_info_from_linkedin(
        self, obj: ObservedObject, phone_number: str
    ) -> ObservedObject:
        db_name = db_name_settings.DB_LINKEDIN_NAME
        if not db_name:
            return obj

        data = await self._search_in_db(phone_number, db_name)

        if not data:
            return obj

        for obj_data in data:
            if obj_data["linkedin_name"]:
                fio = ObjectFio(full_name=obj_data["linkedin_name"])
                obj.fios.append(fio)
            if obj_data["linkedin_email"]:
                obj.emails.append(obj_data["linkedin_email"])
            if obj_data["linkedin_link"]:
                obj.linkedin_link = obj_data["linkedin_link"]

        return obj

    async def get_info_from_rfcont(
        self, obj: ObservedObject, phone_number: str
    ) -> ObservedObject:
        db_name = db_name_settings.DB_RFCONT_NAME
        if not db_name:
            return obj

        data = await self._search_in_db(phone_number, db_name)

        if not data:
            return obj

        for obj_data in data:
            if obj_data["rfcont_name"]:
                fio = ObjectFio(full_name=obj_data["rfcont_name"])
                obj.fios.append(fio)
            if obj_data["rfcont_email"]:
                obj.emails.append(obj_data["rfcont_email"])

        return obj

    async def get_info_from_vtb(
        self, obj: ObservedObject, phone_number: str
    ) -> ObservedObject:
        db_name = db_name_settings.DB_VTB_NAME
        if not db_name:
            return obj

        data = await self._search_in_db(phone_number, db_name)

        if not data:
            return obj

        if data:
            obj.is_vtb = True

        return obj

    async def get_info_from_wildberries(
        self, obj: ObservedObject, phone_number: str
    ) -> ObservedObject:
        db_name = db_name_settings.DB_WILDBERRIES_NAME
        if not db_name:
            return obj

        data = await self._search_in_db(phone_number, db_name)

        if not data:
            return obj

        for obj_data in data:
            if obj_data["wildberries_name"]:
                fio = ObjectFio(full_name=obj_data["wildberries_name"])
                obj.fios.append(fio)
            if obj_data["wildberries_email"]:
                obj.emails.append(obj_data["wildberries_email"])
            if obj_data["wildberries_address"]:
                obj.wildberries_addresses.append(obj_data["wildberries_address"])

        return obj

    async def get_info_from_beeline(
        self, obj: ObservedObject, phone_number: str
    ) -> ObservedObject:
        db_name = db_name_settings.DB_BEELINE_NAME
        if not db_name:
            return obj

        data = await self._search_in_db(phone_number, db_name)

        if not data:
            return obj

        for obj_data in data:
            if obj_data["beeline_full_name"]:
                fio = ObjectFio(full_name=obj_data["beeline_full_name"])
                obj.fios.append(fio)

            address = (
                obj_data.get("beeline_address_city", "")
                + " "
                + obj_data.get("beeline_address_street", "")
                + " "
                + obj_data.get("beeline_address_house", "")
            )
            obj.addresses.append(address)

            if obj_data["beeline_inet_info"]:
                obj.beeline_tariff = obj_data["beeline_inet_info"]

        return obj

    async def get_info_from_mailru(
        self, obj: ObservedObject, phone_number: str
    ) -> ObservedObject:
        db_name = db_name_settings.DB_MAILRU_NAME
        if not db_name:
            return obj

        data = await self._search_in_db(phone_number, db_name)

        if not data:
            return obj

        for obj_data in data:
            if obj_data["mailru_full_name"]:
                fio = ObjectFio(full_name=obj_data["mailru_full_name"])
                obj.fios.append(fio)

            obj.emails.append(obj_data["mailru_email"])

            if obj_data["mailru_education"]:
                obj.educations = obj_data["mailru_education"]

        return obj

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
