import json

import pytest
from django.conf import settings

from network.models import (
    Person,
    Company,
    School,
    WorkExperience,
    EducationExperience,
)
from network.services import ProfileParser

DATA_DIR = settings.BASE_DIR / 'ice-breaker/network/tests/data/'
with open(DATA_DIR / 'profile.json', 'r') as f:
    PROFILE = json.load(f)


@pytest.fixture(scope='module')
def profile():
    return ProfileParser.extract_profile(PROFILE)


@pytest.fixture(scope='module')
def work_experiences():
    return ProfileParser.extract_work_experiences(PROFILE)


@pytest.fixture(scope='module')
def education_history():
    return ProfileParser.extract_education_history(PROFILE)


class TestExtractProfile:
    def test_return_type(self, profile):
        assert type(profile) == dict

    @pytest.mark.django_db
    def test_returns_valid_args(self, profile):
        # should not raise errors
        p = Person(**profile)
        p.save()

    def test_extracts_the_correct_values(self, profile):
        p = Person(**profile)
        assert p.first_name == 'Eugénie'
        assert p.last_name == 'Khayat'
        assert p.linkedin_identifier == 'eugénie-khayat-535085191'
        assert p.country == 'France'
        assert p.city == 'Greater Paris Metropolitan Region'
        assert p.skills == ['PHP', 'JavaScript']


class TestExtractWorkExperiences:
    def test_return_type(self, work_experiences):
        assert type(work_experiences) == list

    def test_parse_the_correct_count(self, work_experiences):
        assert len(work_experiences) == 4

    @pytest.mark.django_db
    def test_returns_valid_args(self, work_experiences):
        # should not raise errors
        for work_experience in work_experiences:
            person, _ = Person.objects.get_or_create(
                linkedin_identifier=work_experience['person']
            )
            company, _ = Company.objects.get_or_create(
                linkedin_url=work_experience['company']['linkedin_url'],
                name=work_experience['company']['name'],
            )
            w = WorkExperience(
                person=person,
                company=company,
                title=work_experience['title'],
                start_year=work_experience['start_year'],
                end_year=work_experience['end_year'],
            )
            w.save()


class TestExtractEducationHistory:
    def test_return_type(self, education_history):
        assert type(education_history) == list

    def test_parse_the_correct_count(self, education_history):
        assert len(education_history) == 6

    @pytest.mark.django_db
    def test_returns_valid_args(self, education_history):
        # should not raise errors
        for education in education_history:
            person, _ = Person.objects.get_or_create(
                linkedin_identifier=education['person']
            )
            school, _ = School.objects.get_or_create(
                linkedin_url=education['school']['linkedin_url'],
                name=education['school']['name'],
            )
            e = EducationExperience(
                person=person,
                school=school,
                field_of_study=education['field_of_study'],
                start_year=education['start_year'],
                end_year=education['end_year'],
            )
            e.save()
