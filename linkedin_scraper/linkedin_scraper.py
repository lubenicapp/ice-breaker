from datetime import datetime
import json

import requests

from django.conf import settings


class LinkedinScraper:
    API_ENDPOINT: str = settings.PROXYCURL_API_ENDPOINT
    HEADERS = {'Authorization': f'Bearer {settings.PROXYCURL_API_KEY}'}

    @classmethod
    def get_profile(cls, linkedin_url: str) -> dict:
        response = requests.get(
            cls.API_ENDPOINT + '/proxycurl/api/v2/linkedin',
            headers=cls.HEADERS,
            params={'linkedin_profile_url': linkedin_url}
        )
        cls.save_data(response.json(), linkedin_url.strip('/').split('/')[-1].split('?')[0])
        return response.json()


    @staticmethod
    def save_data(data, slug):
        with open(f'dump/{slug}-{datetime.now().second}.json', 'w') as f:
            json.dump(data, f, indent=4)
