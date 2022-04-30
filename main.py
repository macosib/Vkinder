from time import sleep
import time

import requests
import config
import webbrowser
import pprint


class VkApi:

    def __init__(self):
        self.token = self._check_valid_token()
        self.params = {
            'access_token': self.token,
            'v': '5.131'
        }
        self.offset = 0

    def _access_code(self):
        endpoint = 'https://oauth.vk.com/authorize'
        params = {
            'client_id': config.app_id,
            'display': 'page',
            'redirect_uri': config.redirect_uri,
            'scope': config.scope,
            'response_type': 'code',
            'v': '5.131'
        }
        try:
            responce = requests.get(url=endpoint, params=params)
            responce.raise_for_status()
            if responce.status_code != 200:
                raise Exception('Ошибка при получени кода')
            webbrowser.open(responce.url)
            code = input('Введите код с браузера: ').split('code=')[1]
            return code
        except:
            print('Ошибка при получении кода')

    def _access_token(self):
        endpoint = 'https://oauth.vk.com/access_token'
        params = {
            'client_id': config.app_id,
            'client_secret': config.client_secret,
            'redirect_uri': config.redirect_uri,
            'code': self._access_code()
        }
        try:
            responce = requests.get(url=endpoint, params=params)
            responce.raise_for_status()
            if responce.status_code != 200:
                raise Exception('Ошибка при получении токена')
            with open('token.txt', 'w', encoding='utf-8') as file:
                file.write(responce.json()['access_token'])
            return responce.json()['access_token']
        except:
            print('Ошибка при получении токена')

    def _check_valid_token(self):
        with open('token.txt', 'r', encoding='utf-8') as file:
            accses_token = file.read().strip()
        endpoint = f'{config.base_url}secure.checkToken'
        params = {
            'access_token': config.service_key,
            'token': accses_token,
            'v': '5.131'
        }
        responce = requests.get(url=endpoint, params=params)
        if accses_token and responce.json().get('response').get('success') == 1:
            return accses_token
        else:
            return self._access_token()

    def _get_city_id(self, city_name):
        endpoint = f'{config.base_url}database.getCities'
        params = {
            'country_id': '1',
            'q': city_name,
            'count': 1
        }
        responce = requests.get(url=endpoint, params={**params, **self.params})
        return responce.json()['response']['items'][0]['id']

    def get_users(self, city='Новосибирск', sex=1, age=30, count=100):
        endpoint = f'{config.base_url}users.search'
        params = {
            'offset': self.offset,
            'count': count,
            'city': self._get_city_id(city),
            'sex': sex,
            'age_from': age,
            'age_to': age,
            'has_photo': 1
        }
        responce = requests.get(url=endpoint, params={**params, **self.params})
        self.offset += 100
        return responce.json()

    def get_user_info(self, user_id):
        endpoint = f'{config.base_url}users.get'
        params = {
            'user_ids': user_id,
            'fields': 'bdate,sex,city,relation'
        }
        responce = requests.get(url=endpoint, params={**params, **self.params})
        return responce.json()

    def __max_size_foto_filter(self, photos):
        result = {}
        logs_file = []
        for foto in photos.json()['response']['items']:
            max_size_photo = foto['sizes'][-1]
            current_time = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime(foto['date']))

            if f"{foto['likes']['count']}.jpg" in result:
                result.update({f"{foto['likes']['count']} {current_time}.jpg": max_size_photo})
                logs_file.extend([{'file_name': f"{foto['likes']['count']} {current_time}.jpg",
                                   'size': f"{max_size_photo['height']}x{max_size_photo['width']}"}])
            else:
                result.update({f"{foto['likes']['count']}.jpg": max_size_photo})
                logs_file.extend([{'file_name': f"{foto['likes']['count']}.jpg",
                                   'size': f"{max_size_photo['height']}x{max_size_photo['width']}"}])
        return result, logs_file

    def get_photos_from_profile(self, user_id=8487111, album_id='profile'):
        endpoint = f'{config.base_url}photos.get'
        params = {
            'owner_id': user_id,
            'album_id': album_id,
            'extended': 1,
        }
        response = requests.get(endpoint, params={**self.params, **self.params, **params})
        response.raise_for_status()
        time.sleep(0.33)
        if response.status_code == 200:
            print(f'Список фотографий со профиля id{user_id} получен')
        print(response.json())
        return self.__max_size_foto_filter(response)


def main():
    user_id = 'yarowoe'
    # user_city = input('Введите город: ')
    # user_sex = int(input('Введите пол, 1 — Женщина; 2 — Мужчина; 0 — Любой: '))
    # age = int(input('Введите возраст: '))
    vk_1 = VkApi()
    print(vk_1.get_photos_from_profile())
    # pprint.pprint(vk_1.get_users('Новосибирск', 1, 25))
    # sleep(5)
    # print()
    # print()
    # pprint.pprint(vk_1.get_users())
    # sleep(5)
    # print()
    # print()
    # pprint.pprint(vk_1.get_users())
    # pprint.pprint(vk_1.get_user_info(user_id))


if __name__ == '__main__':
    main()
