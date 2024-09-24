class PersonParser:
    @classmethod
    def parse(cls, data: dict) -> dict:
        return {
            'linkedin_identifier': data['public_identifier'],
            'first_name': data['first_name'],
            'last_name': data['last_name'],
            'profile_picture_url': data['profile_pic_url'],
            'country': data['country_full_name'],
            'city': data['city'],
            'skills': data['skills'],
            'birth_date': data['birth_date']
        }
