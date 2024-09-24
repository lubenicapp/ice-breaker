import json
from django.conf import settings

from network.models import Person
from network.services import PersonParser

DATA_DIR = settings.BASE_DIR / 'ice-breaker/network/tests/data/'
with open(DATA_DIR / 'profile.json', 'r') as f:
    PROFILE = json.load(f)


class TestPersonParser:
    def test_person_parser_return_type(self):
        assert type(PersonParser.parse(PROFILE)) == Person
