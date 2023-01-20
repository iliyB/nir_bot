from typing import Any, Set

from aiogram import html
from our_types import ObservedStrObject
from py_singleton import singleton
from schemes.objects import ObservedObject


@singleton
class CardService:
    def create_card(self, obj: ObservedObject) -> ObservedStrObject:
        names = self._get_obj_names_str(obj)
        phones = self._get_obj_phones_str(obj)
        emails = self._get_obj_emails_str(obj)
        addresses = self._get_obj_addresses_str(obj)
        birthdays = self._get_obj_birthdays_str(obj)

        vk = self._get_obj_vk_str(obj)
        ok = self._get_obj_ok_str(obj)
        youtube = self._get_obj_youtube_str(obj)
        rutube = self._get_obj_rutube_str(obj)

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
        cars = self._get_obj_cars_str(obj)

        yandex_orders = self._get_delivery_str(
            "Яндекс доставка", obj, "yandex_delivery_orders"
        )
        delivery_orders = self._get_delivery_str(
            "Деливери клаб доставка", obj, "delivery_club_delivery_orders"
        )
        sushi_orders = self._get_delivery_str(
            "Суши доставка", obj, "sushi_delivery_orders"
        )
        # two_berega_orders = self._get_delivery_str(
        #     "Два берега доставка", obj, "two_berega_delivery_orders"
        # )

        observed_str_object = ObservedStrObject(
            main_info="\n\n".join([names, phones, emails, addresses, birthdays, ""]),
            extract_info="\n\n".join(
                [
                    wildberries_addresses,
                    educations,
                    linkedin_link,
                    pikabu_username,
                    is_vtb,
                    beeline_tariff,
                    "",
                ]
            ),
            cars_info=cars + "\n\n",
            delivery_info="\n\n".join([yandex_orders, delivery_orders, sushi_orders])
            + "\n\n",
            links_info="\n\n".join([vk, ok, youtube, rutube]),
        )
        return observed_str_object

    @staticmethod
    def _get_value_from_simple_field(title: str, value: Any) -> str:
        if value is None or value is False:
            return f"{html.bold(title)}: ----"

        if isinstance(value, bool) and value:
            return f"{html.bold(title)}: Да"

        return f"{html.bold(title)}: {str(value)}"

    def _get_obj_names_str(self, obj: ObservedObject) -> str:
        return self._from_set_to_str_list(
            title="Возможные имена", data_set=set(obj.fios)
        )

    def _get_obj_emails_str(self, obj: ObservedObject) -> str:
        return self._from_set_to_str_list(
            title="Возможные почтыe ящики", data_set=set(obj.emails)
        )

    def _get_obj_phones_str(self, obj: ObservedObject) -> str:
        return self._from_set_to_str_list(
            title="Возможные телефонные номера", data_set=set(obj.phones)
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

    def _get_obj_vk_str(self, obj: ObservedObject) -> str:
        return self._from_set_to_str_list(
            title="Возможные аккаунты вк", data_set=set(obj.vk_links)
        )

    def _get_obj_ok_str(self, obj: ObservedObject) -> str:
        return self._from_set_to_str_list(
            title="Возможные аккаунты в ok", data_set=set(obj.ok_links)
        )

    def _get_obj_youtube_str(self, obj: ObservedObject) -> str:
        return self._from_set_to_str_list(
            title="Возможные аккаунты в youtube", data_set=set(obj.youtube_links)
        )

    def _get_obj_rutube_str(self, obj: ObservedObject) -> str:
        return self._from_set_to_str_list(
            title="Возможные аккаунты в rutube", data_set=set(obj.rutube_links)
        )

    @staticmethod
    def _get_delivery_str(
        title: str, obj: ObservedObject, delivery_orders_param_name: str
    ) -> str:
        deliveries_str = ""
        sum_orders = 0

        for delivery_order in getattr(obj, delivery_orders_param_name):
            if (
                not delivery_order.customer_name
                and not delivery_order.date
                and not delivery_order.address
                and not delivery_order.comment
                and not delivery_order.order_sum
            ):
                continue
            deliveries_str += (
                f"\nКлиент - {delivery_order.customer_name}\n"
                + f"Дата - {str(delivery_order.date)}\n"
                + f"Адрес - {delivery_order.address}\n"
                + f"Комментарий - {delivery_order.comment}\n"
                + f"Сума заказа - {delivery_order.order_sum}\n"
            )
            sum_orders = max(
                sum_orders,
                delivery_order.orders_sum if delivery_order.orders_sum else 0,
            )

        if not deliveries_str:
            deliveries_str = "\n" + "-" * 30
        else:
            deliveries_str += f"\nСуммарная сумма заказов - {sum_orders}"

        return f"{html.bold(title)}:{deliveries_str}"

    @staticmethod
    def _get_obj_cars_str(obj: ObservedObject) -> str:
        cars_str = ""

        for car in obj.cars:
            cars_str += (
                f"\nГос. номер - {car.number}\n"
                + f"Старый гос. номер - {car.old_number}\n"
                + f"Модель - {car.model}\n"
                + f"Цвет - {car.color}\n"
                + f"Год выпуска - {car.release_year}\n"
                + f"Владелец - {car.owner_name}\n"
                + f"Дата рождения владельца - {car.owner_birthday}\n"
                + f"Права - {car.place_if_driver_license}\n"
            )

        if not cars_str:
            cars_str = "\n" + "-" * 30

        return f"{html.bold('Автомобили')}:{cars_str}"

    @staticmethod
    def _from_set_to_str_list(title: str, data_set: Set[Any]) -> str:
        str_list = "".join([("\n" + str(data)) for data in data_set])

        if not str_list:
            str_list = "\n" + "-" * 30

        return f"{html.bold(title)}:{str_list}"
