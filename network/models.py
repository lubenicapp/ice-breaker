from django.db import models
from django.core.mail import send_mail
from django.utils.text import slugify

from hrid import HRID


class Person(models.Model):
    linkedin_identifier = models.CharField(max_length=120, null=True)
    first_name = models.CharField(max_length=127)
    last_name = models.CharField(max_length=127)
    profile_picture_url = models.URLField(null=True)
    country = models.CharField(max_length=127, null=True)
    city = models.CharField(max_length=127, null=True)
    skills = models.JSONField(null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def prefixed_id(self):
        return f'p-{self.id}'

    @property
    def as_node(self):
        return {
            'id': self.prefixed_id(),
            'img': self.profile_picture_url,
            'name': f'{self.first_name} {self.last_name}'
        }


class Company(models.Model):
    linkedin_url = models.URLField(null=True)
    name = models.CharField(max_length=127)
    profile_picture_url = models.URLField(null=True)
    location = models.CharField(max_length=127, null=True)

    def prefixed_id(self):
        return f'c-{self.id}'

    @property
    def as_node(self):
        return {
            'id': self.prefixed_id(),
            'img': 'https://hookmap.s3.eu-west-1.amazonaws.com/blue_ball.png',
            'name': f'{self.name}'
        }

class School(models.Model):
    linkedin_url = models.URLField(null=True)
    name = models.CharField(max_length=127)
    profile_picture_url = models.URLField(null=True)

    def prefixed_id(self):
        return f's-{self.id}'

    @property
    def as_node(self):
        return {
            'id': self.prefixed_id(),
            'img': 'https://hookmap.s3.eu-west-1.amazonaws.com/yellow_ball.png',
            'name': f'{self.name}'
        }

class WorkExperience(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='work_experiences')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='work_experiences')
    title = models.CharField(max_length=127)
    start_year = models.PositiveSmallIntegerField(null=True)
    end_year = models.PositiveSmallIntegerField(null=True)

    @property
    def as_link(self):
        return {
            'source': self.person.prefixed_id(),
            'target': self.company.prefixed_id()
        }

class EducationExperience(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='education_experiences')
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='education_experiences')
    field_of_study = models.CharField(max_length=127, null=True)
    start_year = models.PositiveSmallIntegerField(null=True)
    end_year = models.PositiveSmallIntegerField(null=True)

    @property
    def as_link(self):
        return {
            'source': self.person.prefixed_id(),
            'target': self.school.prefixed_id()
        }

class Network(models.Model):
    slug = models.SlugField(unique=True)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=127, null=True)
    credits = models.PositiveSmallIntegerField(default=0)
    persons = models.ManyToManyField(Person, related_name='networks')
    companies = models.ManyToManyField(Company, related_name='networks')
    schools = models.ManyToManyField(School, related_name='networks')

    def save(self, *args, **kwargs):
        if not self.slug:
            h = HRID()
            self.slug = slugify(h.generate())
            try:
                send_mail('', self.slug, None, [self.email])
            except (ConnectionError, Exception):
                pass

        super().save(*args, **kwargs)
