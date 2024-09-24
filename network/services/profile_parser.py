from typing import List
from network.models import Person, Company, School, WorkExperience, EducationExperience


class ProfileParser:
    @classmethod
    def ingest_profile_data(cls, data: dict):
        extracted_profile = cls.extract_profile(data)
        p = cls.__build_person(extracted_profile)

        work_experiences = cls.extract_work_experiences(data)
        cls.__build_work_experiences(work_experiences, p)

        education_history = cls.extract_education_history(data)
        cls.__build_education_history(education_history, p)

    @staticmethod
    def __build_person(data):
        p, _ = Person.objects.update_or_create(
            linkedin_identifier=data['linkedin_identifier'],
            defaults={**data},
        )
        return p

    @staticmethod
    def __build_work_experiences(work_experiences, person):
        for work_experience in work_experiences:
            company, _ = Company.objects.update_or_create(
                linkedin_url=work_experience['company']['linkedin_url'],
                defaults={'name':work_experience['company']['name']},
            )
            w = WorkExperience(
                person=person,
                company=company,
                title=work_experience['title'],
                start_year=work_experience['start_year'],
                end_year=work_experience['end_year'],
            )
            w.save()

    @staticmethod
    def __build_education_history(education_history, person):
        for education in education_history:
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

    @classmethod
    def extract_profile(cls, data: dict) -> dict:
        return {
            'linkedin_identifier': data['public_identifier'],
            'first_name': data['first_name'],
            'last_name': data['last_name'],
            'profile_picture_url': data['profile_pic_url'],
            'country': data['country_full_name'],
            'city': data['city'],
            'skills': data['skills'],
        }

    @classmethod
    def extract_work_experiences(cls, data: dict) -> List[dict]:
        experiences = data.get('experiences', [])
        return [
            {
                'person': data['public_identifier'],
                'company': {
                    'name': experience['company'],
                    'linkedin_url': experience['company_linkedin_profile_url'],
                },
                'title': experience['title'],
                'start_year': experience['starts_at']['year']
                if experience['starts_at']
                else None,
                'end_year': experience['ends_at']['year']
                if experience['ends_at']
                else None,
            }
            for experience in experiences
        ]

    @classmethod
    def extract_education_history(cls, data: dict) -> List[dict]:
        education_history = data.get('education', [])
        return [
            {
                'person': data['public_identifier'],
                'school': {
                    'name': education['school'],
                    'linkedin_url': education['school_linkedin_profile_url'],
                },
                'field_of_study': education['field_of_study'],
                'start_year': education['starts_at']['year']
                if education['starts_at']
                else None,
                'end_year': education['ends_at']['year']
                if education['ends_at']
                else None,
            }
            for education in education_history
        ]
