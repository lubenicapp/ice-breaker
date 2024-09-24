from django.db import models
from django.core.mail import send_mail
from django.utils.text import slugify

from hrid import HRID


class Person(models.Model):
    linkedin_identifier = models.URLField()
    first_name = models.CharField(max_length=127)
    last_name = models.CharField(max_length=127)
    profile_picture_url = models.URLField(null=True)
    country = models.CharField(max_length=127, null=True)
    city = models.CharField(max_length=127, null=True)
    skills = models.JSONField(null=True)
    updated_at = models.DateTimeField(auto_now=True)

class Company(models.Model):
    linkedin_url = models.URLField(null=True)
    name = models.CharField(max_length=127)
    profile_picture_url = models.URLField(null=True)
    location = models.CharField(max_length=127, null=True)


class School(models.Model):
    linkedin_url = models.URLField(null=True)
    name = models.CharField(max_length=127)
    profile_picture_url = models.URLField(null=True)


class WorkExperience(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    title = models.CharField(max_length=127)
    start_year = models.PositiveSmallIntegerField(null=True)
    end_year = models.PositiveSmallIntegerField(null=True)


class EducationExperience(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    field_of_study = models.CharField(max_length=127, null=True)
    start_year = models.PositiveSmallIntegerField(null=True)
    end_year = models.PositiveSmallIntegerField(null=True)


class Network(models.Model):
    slug = models.SlugField(unique=True)
    email = models.EmailField(unique=True)
    credits = models.PositiveSmallIntegerField(default=0)
    persons = models.ManyToManyField(Person, related_name='networks')
    companies = models.ManyToManyField(Company, related_name='networks')
    schools = models.ManyToManyField(School, related_name='networks')

    def save(self, *args, **kwargs):
        if not self.slug:
            h = HRID()
            self.slug = slugify(h.generate())
            send_mail('', self.slug, None, [self.email])

        super().save(*args, **kwargs)
