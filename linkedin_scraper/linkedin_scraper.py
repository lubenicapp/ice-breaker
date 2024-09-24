import os

class LinkedinScraper:
    API_ENDPOINT: str = os.getenv('PROXYCURL_API_ENDPOINT')
    HEADERS = {'Authorization': f'Bearer {os.getenv('PROXYCURL_API_KEY')}'}

    @classmethod
    def get_profile(cls, linkedin_url: str) -> dict:
        ...
