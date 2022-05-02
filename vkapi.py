from time import sleep
import requests
import config
import webbrowser
from random import randint


class VkApi:

    def __init__(self):
        self.token = self._check_valid_token()
        # self.token = config.token_vkinder
        self.params = {
            'access_token': self.token,
            'v': '5.131'
        }
        self.offset = 30

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
        print(response.json())
        sleep(0.33)
        return response.json()['response']['items'][0]['id']

    def users_search_res(self, search_result, city):
        result = []
        for person in search_result['response']['items']:
            if person['is_closed'] is True \
                    or person.get('city') is None\
                    or person.get('city').get('title') != city:
                continue
            result.append({
                'first_name': person.get('first_name'),
                'last_name': person.get('last_name'),
                'person_id': person.get('id'),
                'city_title': person.get('home_town'),
                'sex': person.get('sex'),
                'bdate': person.get('bdate'),
                'profile_foto': self.get_photos_from_profile(person.get('id'))
            })
        return result

    def users_search(self, city, sex, birth_year, count=1):
        endpoint = f'{config.base_url}users.search'
        params = {
            'offset': self.offset,
            'count': count,
            'city': self._get_city_id(city),
            'sex': sex,
            'birth_year': birth_year,
            'has_photo': 1,
            'fields': 'sex, bdate, city'
        }

        try:
            response = requests.get(url=endpoint, params={**params, **self.params})
            response.raise_for_status()
            if response.status_code != 200:
                raise Exception()
            self.offset += count
            return self.users_search_res(response.json(), city)
        except:
            print('Ошибка при поиске пользователей')

    def get_user_info(self, user_id):
        endpoint = f'{config.base_url}users.get'
        params = {
            'user_ids': user_id,
            'fields': 'bdate, sex, home_town'
        }
        response = requests.get(url=endpoint, params={**params, **self.params})
        data = response.json()['response'][0]
        if data.get('home_town', None) is None:
            city = 'Москва'
        else:
            city = data.get('home_town')
        if data.get('bdate', None) is None or len(data.get('bdate').split('.')) < 3:
            bdate = randint(1980, 2000)
        else:
            bdate = int(data.get('bdate').split('.')[2])
        if data.get('sex', None) is None:
            sex = randint(0, 2)
        else:
            sex = data.get('sex')
        return city, sex, bdate

    def _max_size_foto_filter(self, photos):
        result = []
        for foto in sorted(photos.json()['response']['items'], key=lambda x: x['likes']['count'], reverse=True):
            result.append({'foto_id': foto['id'],
                           'owner_id': foto['owner_id'],
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
            return
