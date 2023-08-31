import urllib.parse

import requests


class Api:
    def __init__(self, front_base_url, back_base_url):
        self.front_base_url = front_base_url
        self.back_base_url = back_base_url

    def create_user(self, chat_id, language):
        requests.post(
            url=f'{self.back_base_url}/telegram/',
            json={
                'chat_id': str(chat_id),
                'language': language,
            }
        )

    def get_user(self, chat_id):
        response = requests.get(
            url=f'{self.back_base_url}/telegram/{chat_id}/',
        )
        if not response.ok:
            return {}
        return response.json()

    def change_user(
            self, chat_id, preferences=None, language=None, is_notified=None,
    ):
        data = {}
        if preferences is not None:
            data.update({'preferences': preferences})
        if language is not None:
            data.update({'language': language})
        if is_notified is not None:
            data.update({'is_notified': is_notified})

        response = requests.patch(
            url=f'{self.back_base_url}/telegram/{chat_id}/',
            json=data,
        )
        print(response.json())

    def make_link_to_see_other(self, chat_id):
        preferences = self.get_user(chat_id).get('preferences')
        params = {}
        if preferences.get('number_of_rooms__in'):
            params['rooms'] = preferences.get('number_of_rooms__in')
        if preferences.get('price__gte'):
            params['priceFrom'] = preferences.get('price__gte')
        if preferences.get('price__lte'):
            params['priceTo'] = preferences.get('price__lte')
        if preferences.get('city__icontains'):
            params['city'] = {
                'Warszawa': 'warsaw',
                'Kraków': 'krakow',
            }.get(preferences.get('city__icontains'))

        if preferences.get('district__in'):
            params['district'] = preferences.get('district__in')

        query_string = urllib.parse.urlencode(params)

        return self.front_base_url + '/rent?' + query_string
