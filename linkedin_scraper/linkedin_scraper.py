from datetime import datetime
import json

from loguru import logger
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
        return response.json()


    @staticmethod
    def _save_data(data, slug):
        try:
            with open(f'dump/{slug}-{datetime.now().second}.json', 'w') as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            logger.error(e)
