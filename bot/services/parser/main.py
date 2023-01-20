from google_parser import google_search
import vk_parser
import html

from datetime import date
from typing import List, Optional, Set

from pydantic import BaseModel, Field


class ObjectFio(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    middle_name: Optional[str] = None

    full_name: Optional[str] = None


class DeliveryBaseScheme(BaseModel):
    customer_name: Optional[str] = None
    date: Optional[date] = None
    address: Optional[str] = None
    comment: Optional[str] = None
    order_sum: Optional[float] = None
    orders_sum: Optional[float] = None
    restaurant: Optional[str] = None

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
    fios: List[Optional[str]] = ["Юрий Монахов"]

    phones: List[str] = []
    emails: List[str] = []
    addresses: List[Optional[str]] = []

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

    searched_by: Set[str] = set()  # По чему уже проводился поиск

# Функция получения ссылки на вк из поисковой выдачи
def link_vk_get_login(links):
    link_vk_id = []
    for link in links:
        link = link.replace("https://vk.com/","")
        link = link.replace("https://m.vk.com/","")
        if link.find("wall") < 0 and link.find("event") < 0:
            question = link.find("?")
            if question >= 1:
                link = link[:question]
            if link not in link_vk_id:
                link_vk_id.append(link)
    return link_vk_id

# def google_parser():
#     result_google = google_search(name="Юрий Монахов", city="Владимир", web_society=web_society[0]).search_web_society()
#
#     result_google_links = []
#     for link in result_google:
#         link = link.get("link")
#         # print(link)
#         # link = link[:link.find("?")]
#         # print(link)
#         if link not in result_google_links:
#             if link.find("search?") <= 0 and link.find("vk.com/@") <= 0 and link.find(
#                     "vk.com/event") <= 0 and link.find("vk.com/people") <= 0:
#                 result_G_VK_links.append(link)
#     print(result_G_VK_links)


def parser_main(obj:ObservedObject) -> str:

    fios = obj.fios
    city = obj.addresses
    phone = obj.phones



    web_society = ["vk.com", "pikabu.ru", "dzen.ru", "twitter.com", "facebook.com", "habr.ru", "ok.ru", "youtube.com", "rutube.ru"]

    # Поиск страницы ВКонтакте через гугл
    result_G_VK = google_search(name=obj.fios, city=obj.address, web_society=web_society[0]).search_web_society()

    result_G_VK_links = []
    for link in result_G_VK:
        link = link.get("link")
        # print(link)
        # link = link[:link.find("?")]
        # print(link)
        if link not in result_G_VK_links:
            if link.find("search?") <= 0 and link.find("vk.com/@") <= 0 and  link.find("vk.com/people") <= 0:
                result_G_VK_links.append(link)
    print("Возможные источники на сайте ВКонтакте", result_G_VK_links)
    vk_users = []
    links_vk_id = link_vk_get_login(result_G_VK_links)
    # print(links_vk_id)
    for id in links_vk_id: 
        try:
            person_vk_info = vk_parser.get_user_info(id)
            print(person_vk_info)
            if fios
            vk_users.append(id)
        except:
            print("Неверный айди")
    print("Подходящие под описание аккаунты ВКонтакте", vk_users, "\n")

    # Поиск по Одноклассникам
    result_G_OK = google_search(name=obj.fios, city=obj.address, web_society=web_society[6]).search_web_society()
    result_G_OK_links = []
    for link in result_G_OK:
        link = link.get("link")
        # print(link)
        # link = link[:link.find("?")]
        # print(link)
        if link not in result_G_OK_links:
            if link.find("search") <= 0 and link.find("vk.com/@") <= 0 and link.find(
                    "vk.com/event") <= 0 and link.find("vk.com/people") <= 0 and link.find("ok.ru/group") <= 0 and link.find("statuses") <= 0:
                result_G_OK_links.append(link)
    print("Ссылки одноклассники", result_G_OK_links)


    # Поиск по ЮТУБ
    result_G_YOUTUBE = google_search(name=obj.fios, city=obj.address, web_society=web_society[7]).search_web_society()
    result_G_YOUTUBE_links = []
    for link in result_G_YOUTUBE:
        link = link.get("link")
        # print(link)
        # link = link[:link.find("?")]
        # print(link)
        if link not in result_G_YOUTUBE_links:
            if link.find("search") <= 0 and link.find("vk.com/@") <= 0 and link.find(
                    "vk.com/event") <= 0 and link.find("vk.com/people") <= 0 and link.find(
                "ok.ru/group") <= 0 and link.find("statuses") <= 0:
                result_G_YOUTUBE_links.append(link)
    print(result_G_YOUTUBE_links)

    # Поиск по РУТУБ
    result_G_RUTUBE = google_search(name=obj.fios, city=obj.address,
                                     web_society=web_society[8]).search_web_society()
    result_G_RUTUBE_links = []
    for link in result_G_RUTUBE:
        link = link.get("link")
        # print(link)
        # link = link[:link.find("?")]
        # print(link)
        if link not in result_G_RUTUBE_links:
            if link.find("search") <= 0 and link.find("vk.com/@") <= 0 and link.find(
                    "vk.com/event") <= 0 and link.find("vk.com/people") <= 0 and link.find(
                "ok.ru/group") <= 0 and link.find("statuses") <= 0:
                result_G_RUTUBE_links.append(link)
    print(result_G_RUTUBE_links)

if __name__ == '__main__':
    parser_main(ObservedObject)