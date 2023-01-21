# import vk_parser
from operator import itemgetter

from schemes.objects import ObservedObject

# Функция получения ссылки на вк из поисковой выдачи
from services.parser import vk_parser
from services.parser.google_parser import google_search


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
    if obj.unique_names:
        fios = max(obj.unique_names, key=len)
    else:
        fios = None

    new_phones = [x for x in obj.phones if x not in obj.searched_by]

    phone = new_phones[0] if new_phones else None

    if obj.priority_address:
        city = obj.priority_address.split(",")[0] if obj.priority_address else None
    else:
        city = None

    birthdays = str(obj.birthdays) if obj.birthdays else None

    if (not fios and not phone) or (not birthdays and not city):
        return

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
        name=fios, city=city, web_society=web_society[0]
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

    #     print("Возможные источники на сайте ВКонтакте", result_G_VK_links)
    vk_users = []
    links_vk_id = link_vk_get_login(result_G_VK_links)
    print(links_vk_id)
    points_vk = {}
    for id in links_vk_id:
        try:
            person_vk_info = vk_parser.get_user_info(id)
            # print(person_vk_info)
            points_vk[id] = 0
            if fios and fios == (
                person_vk_info["response"][0]["first_name"]
                + " "
                + person_vk_info["response"][0]["last_name"]
            ):
                points_vk[id] += 1
                print("Фамилия и Имя сошлись")
            vk_phone = person_vk_info["response"][0]["mobile_phone"]
            vk_phone = vk_phone.replace("+", "")
            vk_phone = vk_phone.replace("-", "")
            vk_phone = vk_phone.replace("(", "")
            vk_phone = vk_phone.replace(")", "")
            # print(vk_phone)
            if phone and phone == vk_phone:
                points_vk[id] += 3
                print("Телефоны сошлись")
            if city and city == person_vk_info["response"][0]["city"]["title"]:
                points_vk[id] += 1
                print("Города сошлись")
            if birthdays and birthdays == person_vk_info["response"][0]["bdate"]:
                points_vk[id] += 2
                print("День рождения сошелся")
            vk_users.append(id)
        except:
            print("Неверный айди")
    # print(points_vk.items())
    vk_users = sorted(points_vk.items(), key=itemgetter(1))
    # print(vk_users)
    vk_users = list(reversed(vk_users))
    # print(vk_users)

    print(
        "Подходящие под описание аккаунты ВКонтакте по уменьшению вероятности",
        vk_users,
        "\n",
    )

    obj.vk_users = [f"https://vk.com/{i}" for i, _ in vk_users]

    obj.vk_links = [i for i in obj.vk_links if i not in obj.vk_users]

    # Поиск по Одноклассникам
    result_G_OK = google_search(
        name=fios, city=city, phone=phone, web_society=web_society[6]
    ).search_web_society()
    # >>>>>>> 0b9a3ef3eb19977f5354eeb7c1ed3ce0608e9123
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
        name=fios, city=city, web_society=web_society[7]
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
    # <<<<<<< HEAD
    #     result_G_RUTUBE = google_search(
    #         name=obj.fios, city=city, web_society=web_society[8]
    #     ).search_web_society()
    # =======
    result_G_RUTUBE = google_search(
        name=fios, city=city, web_society=web_society[8]
    ).search_web_society()
    # >>>>>>> 0b9a3ef3eb19977f5354eeb7c1ed3ce0608e9123
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
