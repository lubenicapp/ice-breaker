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
from network.models import Person, Company, School, WorkExperience, EducationExperience, Network


DATA_DIR = settings.BASE_DIR / 'ice-breaker/network/tests/data/'
with open(DATA_DIR / 'profile.json', 'r') as f:
    PROFILE = json.load(f)


@pytest.fixture
def clear_database():
    for table in [Person, Company, School, WorkExperience, EducationExperience, Network]:
        table.objects.all().delete()



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


class TestIngestProfileData:
    @pytest.mark.django_db
    def test_creates_a_record_for_new_profile(self, clear_database):
        ProfileParser.ingest_profile_data(PROFILE)
        assert Person.objects.count() == 1

    @pytest.mark.django_db
    def test_updates_a_record_for_existing_profile(self, clear_database):
        Person.objects.create(linkedin_identifier='eugénie-khayat-535085191', first_name='Joe')

        ProfileParser.ingest_profile_data(PROFILE)
        p = Person.objects.all()[0]

        assert p.first_name == 'Eugénie'

    @pytest.mark.django_db
    def test_creates_companies(self, clear_database):
        ProfileParser.ingest_profile_data(PROFILE)
        assert Company.objects.count() == 4

    @pytest.mark.django_db
    def test_updates_companies(self, clear_database):
        Company.objects.create(linkedin_url='https://www.linkedin.com/company/aduneo', name='Fake')

        ProfileParser.ingest_profile_data(PROFILE)
        company = Company.objects.get(linkedin_url='https://www.linkedin.com/company/aduneo')

        assert Company.objects.count() == 4
        assert company.name == 'Aduneo'

    @pytest.mark.django_db
    def test_creates_work_experiences(self, clear_database):
        ProfileParser.ingest_profile_data(PROFILE)
        assert len(WorkExperience.objects.all()) == 4


    @pytest.mark.django_db
    def test_creates_schools(self, clear_database):
        ProfileParser.ingest_profile_data(PROFILE)
        assert len(School.objects.all()) == 4

    @pytest.mark.django_db
    def test_creates_education_experiences(self, clear_database):
        ProfileParser.ingest_profile_data(PROFILE)
        assert len(EducationExperience.objects.all()) == 5
