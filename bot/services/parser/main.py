from schemes.objects import ObservedObject
from services.parser import vk_parser

from .google_parser import google_search


# Функция получения ссылки на вк из поисковой выдачи
def link_vk_get_login(links):
    link_vk_id = []
    for link in links:
        link = link.replace("https://vk.com/", "")
        link = link.replace("https://m.vk.com/", "")
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


def parser_main(obj: ObservedObject) -> None:

    city = obj.addresses[0].split(",")[0] if obj.addresses else None
    # phone = obj.phones

    web_society = [
        "vk.com",
        "pikabu.ru",
        "dzen.ru",
        "twitter.com",
        "facebook.com",
        "habr.ru",
        "ok.ru",
        "youtube.com",
        "rutube.ru",
    ]

    # Поиск страницы ВКонтакте через гугл
    result_G_VK = google_search(
        name=obj.fios, city=city, web_society=web_society[0]
    ).search_web_society()

    result_G_VK_links = []
    for link in result_G_VK:
        link = link.get("link")
        # print(link)
        # link = link[:link.find("?")]
        # print(link)
        if link not in result_G_VK_links:
            if (
                link.find("search?") <= 0
                and link.find("vk.com/@") <= 0
                and link.find("vk.com/people") <= 0
            ):
                result_G_VK_links.append(link)

    obj.vk_links = result_G_VK_links

    # print("Возможные источники на сайте ВКонтакте", result_G_VK_links)
    # vk_users = []
    # links_vk_id = link_vk_get_login(result_G_VK_links)
    # # print(links_vk_id)
    # for id in links_vk_id:
    #     try:
    #         person_vk_info = vk_parser.get_user_info(id)
    #         print(person_vk_info)
    #         if fios:
    #             vk_users.append(id)
    #     except:
    #         print("Неверный айди")
    # print("Подходящие под описание аккаунты ВКонтакте", vk_users, "\n")

    # Поиск по Одноклассникам
    result_G_OK = google_search(
        name=obj.fios, city=city, web_society=web_society[6]
    ).search_web_society()
    result_G_OK_links = []
    for link in result_G_OK:
        link = link.get("link")
        # print(link)
        # link = link[:link.find("?")]
        # print(link)
        if link not in result_G_OK_links:
            if (
                link.find("search") <= 0
                and link.find("vk.com/@") <= 0
                and link.find("vk.com/event") <= 0
                and link.find("vk.com/people") <= 0
                and link.find("ok.ru/group") <= 0
                and link.find("statuses") <= 0
            ):
                result_G_OK_links.append(link)

    obj.ok_links = result_G_OK_links
    # print("Ссылки одноклассники", result_G_OK_links)

    # Поиск по ЮТУБ
    result_G_YOUTUBE = google_search(
        name=obj.fios, city=city, web_society=web_society[7]
    ).search_web_society()
    result_G_YOUTUBE_links = []
    for link in result_G_YOUTUBE:
        link = link.get("link")
        # print(link)
        # link = link[:link.find("?")]
        # print(link)
        if link not in result_G_YOUTUBE_links:
            if (
                link.find("search") <= 0
                and link.find("vk.com/@") <= 0
                and link.find("vk.com/event") <= 0
                and link.find("vk.com/people") <= 0
                and link.find("ok.ru/group") <= 0
                and link.find("statuses") <= 0
            ):
                result_G_YOUTUBE_links.append(link)

    obj.youtube_links = result_G_YOUTUBE_links
    # print(result_G_YOUTUBE_links)

    # Поиск по РУТУБ
    result_G_RUTUBE = google_search(
        name=obj.fios, city=city, web_society=web_society[8]
    ).search_web_society()
    result_G_RUTUBE_links = []
    for link in result_G_RUTUBE:
        link = link.get("link")
        # print(link)
        # link = link[:link.find("?")]
        # print(link)
        if link not in result_G_RUTUBE_links:
            if (
                link.find("search") <= 0
                and link.find("vk.com/@") <= 0
                and link.find("vk.com/event") <= 0
                and link.find("vk.com/people") <= 0
                and link.find("ok.ru/group") <= 0
                and link.find("statuses") <= 0
            ):
                result_G_RUTUBE_links.append(link)

    obj.rutube_links = result_G_RUTUBE_links
    # print(result_G_RUTUBE_links)


if __name__ == "__main__":
    parser_main(ObservedObject)
