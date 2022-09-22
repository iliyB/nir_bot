from typing import Any, Set

from aiogram import html
from py_singleton import singleton
from schemes.objects import ObservedObject


@singleton
class CardService:
    def create_card(self, obj: ObservedObject) -> str:
        names = self._get_obj_names_str(obj)
        emails = self._get_obj_emails_str(obj)
        addresses = self._get_obj_addresses_str(obj)
        birthdays = self._get_obj_birthdays_str(obj)

        wildberries_addresses = self._get_obj_wildberries_addresses_str(obj)
        educations = self._get_obj_educations_str(obj)

        linkedin_link = self._get_value_from_simple_field(
            "Линк linkedin", obj.linkedin_link
        )
        pikabu_username = self._get_value_from_simple_field(
            "Ник на pikabu", obj.pikabu_username
        )
        is_vtb = self._get_value_from_simple_field("Клиент ВТБ", obj.is_vtb)
        beeline_tariff = self._get_value_from_simple_field(
            "Тариф билайн", obj.beeline_tariff
        )

        return "\n\n".join(
            [
                names,
                emails,
                addresses,
                birthdays,
                wildberries_addresses,
                educations,
                linkedin_link,
                pikabu_username,
                is_vtb,
                beeline_tariff,
            ]
        )

    @staticmethod
    def _get_value_from_simple_field(title: str, value: Any) -> str:
        if value is None or value is False:
            return f"{html.bold(title)}: ----"

        if isinstance(value, bool) and value:
            return f"{html.bold(title)}: Да"

        return f"{html.bold(title)}: {str(value)}"

    def _get_obj_names_str(self, obj: ObservedObject) -> str:
        return self._from_set_to_str_list(
            title="Возможные имена", data_set=set([fio.full_name for fio in obj.fios])
        )

    def _get_obj_emails_str(self, obj: ObservedObject) -> str:
        return self._from_set_to_str_list(
            title="Возможные почтыe ящики", data_set=set(obj.emails)
        )

    def _get_obj_addresses_str(self, obj: ObservedObject) -> str:
        return self._from_set_to_str_list(
            title="Возможные адреса", data_set=set(obj.addresses)
        )

    def _get_obj_birthdays_str(self, obj: ObservedObject) -> str:
        return self._from_set_to_str_list(
            title="Возможные дни рождения", data_set=set(obj.birthdays)
        )

    def _get_obj_wildberries_addresses_str(self, obj: ObservedObject) -> str:
        return self._from_set_to_str_list(
            title="Адресса пунктов wildberries", data_set=set(obj.wildberries_addresses)
        )

    def _get_obj_educations_str(self, obj: ObservedObject) -> str:
        return self._from_set_to_str_list(
            title="Образование", data_set=set(obj.educations)
        )

    @staticmethod
    def _from_set_to_str_list(title: str, data_set: Set[Any]) -> str:
        str_list = "".join([("\n" + str(data)) for data in data_set])

        if not str_list:
            str_list = "\n" + "-" * 30

        return f"{html.bold(title)}:{str_list}"
