import json
import pytest
from django.conf import settings

from network.models import Person
from network.services import PersonParser

DATA_DIR = settings.BASE_DIR / 'ice-breaker/network/tests/data/'
with open(DATA_DIR / 'profile.json', 'r') as f:
    PROFILE = json.load(f)


class TestPersonParser:
    def test_person_parser_return_type(self):
        assert type(PersonParser.parse(PROFILE)) == dict

    @pytest.mark.django_db
    def test_person_parser_returns_valid_args(self):
        # should not raise errors
        p = Person(**PersonParser.parse(PROFILE))
        p.save()

    def test_person_parser_parse_the_correct_values(self):
        p = Person(**PersonParser.parse(PROFILE))
        assert p.first_name == 'Eugénie'
        assert p.last_name == 'Khayat'
        assert p.linkedin_identifier == 'eugénie-khayat-535085191'
        assert p.country == 'France'
        assert p.city == 'Greater Paris Metropolitan Region'
        assert p.skills == ['PHP', 'JavaScript']
        assert p.birth_date is None
