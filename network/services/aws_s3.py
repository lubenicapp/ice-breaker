import boto3
from hrid import HRID
import requests
from django.conf import settings
from rest_framework import status

class AWSS3:
    CLIENT = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME,
    )
    BUCKET = settings.AWS_STORAGE_BUCKET_NAME
    GENERATOR = HRID()


    @classmethod
    def upload_image_from_url(cls, image_url):
        try:
            response = requests.get(image_url)
            if response.status_code != status.HTTP_200_OK:
                raise Exception()
            key = cls.GENERATOR.generate()
            cls.CLIENT.put_object(
            Bucket=cls.BUCKET,
            Key=f'{key}.jpeg',
            Body=response.content,
            ContentType='image/jpeg'
            )
        except requests.exceptions.RequestException as e:
            return image_url
        return f'https://{cls.BUCKET}.s3.eu-west-1.amazonaws.com/{key}.jpeg'
