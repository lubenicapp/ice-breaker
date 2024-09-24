from typing import List


class ProfileParser:
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
