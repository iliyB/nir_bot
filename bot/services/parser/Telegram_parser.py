import requests

api = 'https://api.vk.com/method/'
access_token = "vk1.a.h9hRB2VhCtVGq-pO8vbgWbqGtLeGb0M0RCNh_klrXT3t_u0QTI5e7tQtWo0KhX4bfLCRNz9K1tA91Do-NqskrCoALnRO7-jjaGQNXhSV0WsBAlflib7In6xyireIxZwAq_gE4h0rhPa4wJdGpqbBVwZX1l0CcpePg3kVrAlOdtiBMqJcpCzIP4ZTU7nGdSE0"

def get_access_token():
    response = requests.get("https://oauth.vk.com/authorize?client_id=8163455&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=friends,stories,photos,app_widget,groups,docs,manage,wall&response_type=token&v=5.131&state=123456")
    json_response = response.json()
    print("ANSWER", json_response)


def search(query):
    request = api + "search.getHints?q=" + query + "&v=5.131&access_token=" + access_token
    try:
        response = requests.post(request)
        json_response = response.json()
        # python_response = json.load(json_response)
        print("ANSWER", json_response)
    except UnicodeEncodeError:
        print("Введите корректную строку")


def get_user_info(user_id):
    print("GET_USER_INFO")
    # data = '{"email": "' + email + '", "password": "' + password + '"}'
    request = api + "users.get?user_id=" + user_id + "&v=5.131&fields=photo_id, verified, sex, bdate, city, country, home_town, has_photo, photo_50, photo_100, photo_200_orig, photo_200, photo_400_orig, photo_max, photo_max_orig, online, domain, has_mobile, contacts, site, education, universities, schools, status, last_seen, followers_count, common_count, occupation, nickname, relatives, relation, personal, connections, exports, activities, interests, music, movies, tv, books, games, about, quotes, can_post, can_see_all_posts, can_see_audio, can_write_private_message, can_send_friend_request, is_favorite, is_hidden_from_feed, timezone, screen_name, maiden_name, crop_photo, is_friend, friend_status, career, military, blacklisted, blacklisted_by_me, can_be_invited_group" + "&access_token=" + access_token
    # request = api + "account.getProfileInfo?user_id=" + user_id + "&v=5.81" + "&access_token=" + access_token

    # print("req", request)
    response = ""
    try:
        response = requests.post(request)
        json_response = response.json()

        # python_response = json.load(json_response)
        print("ANSWER", json_response)
        print("Страна", json_response['response'][0]['country']['title'])
        print("Город", json_response['response'][0]['city']['title'])
        print("Имя", json_response['response'][0]['first_name'])
        print("Фамилия", json_response['response'][0]['last_name'])
        print("Никнэйм", json_response['response'][0]['nickname'])
        print("Домен (никнэйм)", json_response['response'][0]['domain'])
        print("ANSWER3", response)
    except UnicodeEncodeError:
        print("Введите данные для авторизации на английском языке без пробелов!")

def get_audio_favorite(user_id):
    request = api + "users.get?user_id=" + user_id + "&v=5.81" + "&access_token=" + access_token
    # print("req", request)
    response = ""
    try:
        response = requests.post(request)
        json_response = response.json()
        # python_response = json.load(json_response)
        print("ANSWER", json_response)
        print("ANSWER2", response)
    except UnicodeEncodeError:
        print("Введите данные для авторизации на английском языке без пробелов!")


if __name__ == '__main__':
    get_user_info("yuri_monakhov")
