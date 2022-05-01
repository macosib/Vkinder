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
            response = requests.get(url=endpoint, params=params)
            response.raise_for_status()
            if response.status_code != 200:
                raise Exception()
            webbrowser.open(response.url)
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
            response = requests.get(url=endpoint, params=params)
            response.raise_for_status()
            if response.status_code != 200:
                raise Exception()
            with open('token.txt', 'w', encoding='utf-8') as file:
                file.write(response.json()['access_token'])
            return response.json()['access_token']
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
        response = requests.get(url=endpoint, params={**params, **self.params})
        return response.json()['response']['items'][0]['id']

    def users_search_res(self, search_result):
        result = []
        for person in search_result['response']['items']:
            result.append({
                'first_name': person.get('first_name'),
                'last_name': person.get('last_name'),
                'person_id': person.get('id'),
                'city_id': person.get('city').get('id'),
                'city_title': person.get('city').get('title'),
                'sex': person.get('sex'),
                'bdate': person.get('bdate'),
                'profile_foto': self.get_photos_from_profile(person.get('id'))
            })
        return result


    def users_search(self, city='Новосибирск', sex=1, age=30, count=100):
        endpoint = f'{config.base_url}users.search'
        params = {
            'offset': self.offset,
            'count': count,
            'city': self._get_city_id(city),
            'sex': sex,
            'age_from': age,
            'age_to': age,
            'has_photo': 1,
            'fields': 'sex, bdate, city'
        }
        try:
            response = requests.get(url=endpoint, params={**params, **self.params})
            response.raise_for_status()
            if response.status_code != 200:
                raise Exception()
            self.offset += 100
            return self.users_search_res(response.json())
        except:
            print('Ошибка при поиске пользователей')

    # def get_user_info(self, user_id):
    #     endpoint = f'{config.base_url}users.get'
    #     params = {
    #         'user_ids': user_id,
    #         'fields': 'bdate, sex, city, relation'
    #     }
    #     response = requests.get(url=endpoint, params={**params, **self.params})
    #     return response.json()

    def _max_size_foto_filter(self, photos):
        result = []
        for foto in sorted(photos.json()['response']['items'], key=lambda x: x['likes']['count'], reverse=True):
            result.append({'id': foto['id'],
                           'likes': foto['likes']['count'],
                           'url': foto['sizes'][-1]['url']})
            if len(result) == 3:
                break
        return result

    def get_photos_from_profile(self, user_id):
        sleep(0.33)
        endpoint = f'{config.base_url}photos.get'
        params = {
            'owner_id': user_id,
            'album_id': 'profile',
            'extended': 1,
        }
        try:
            response = requests.get(endpoint, params={**self.params, **self.params, **params})
            response.raise_for_status()
            if response.status_code != 200:
                raise Exception()
            return self._max_size_foto_filter(response)
        except:
            print(f'Ошибка при получении фото профиля {user_id}')


def main():
    user_id = 'yarowoe'
    # user_city = input('Введите город: ')
    # user_sex = int(input('Введите пол, 1 — Женщина; 2 — Мужчина; 0 — Любой: '))
    # age = int(input('Введите возраст: '))
    vk_1 = VkApi()
    # print(*vk_1.get_photos_from_profile(8487111), sep='\n')
    pprint.pprint(vk_1.users_search('Новосибирск', 1, 30, 10))
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
