import json
import pytest
from django.conf import settings

from network.models import Person
from network.services import ProfileParser

DATA_DIR = settings.BASE_DIR / 'ice-breaker/network/tests/data/'
with open(DATA_DIR / 'profile.json', 'r') as f:
    PROFILE = json.load(f)


class TestExtractProfile:
    def test_return_type(self):
        assert type(ProfileParser.extract_profile(PROFILE)) == dict

    @pytest.mark.django_db
    def test_returns_valid_args(self):
        # should not raise errors
        p = Person(**ProfileParser.extract_profile(PROFILE))
        p.save()

    def test_extracts_the_correct_values(self):
        p = Person(**ProfileParser.extract_profile(PROFILE))
        assert p.first_name == 'Eugénie'
        assert p.last_name == 'Khayat'
        assert p.linkedin_identifier == 'eugénie-khayat-535085191'
        assert p.country == 'France'
        assert p.city == 'Greater Paris Metropolitan Region'
        assert p.skills == ['PHP', 'JavaScript']
