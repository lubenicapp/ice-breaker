from django.db import models


class Person(models.Model):
    linkedin_url = models.URLField()
    first_name = models.CharField(max_length=127)
    last_name = models.CharField(max_length=127)
    profile_picture_url = models.URLField(null=True)
    country = models.CharField(max_length=127, null=True)
    city = models.CharField(max_length=127, null=True)
    skills = models.JSONField(null=True)
    birth_date = models.DateField(null=True)


class Company(models.Model):
    linkedin_url = models.URLField()
    name = models.CharField(max_length=127)
    profile_picture_url = models.URLField(null=True)
    industry = models.CharField(max_length=127, null=True)
    location = models.CharField(max_length=127, null=True)

class School(models.Model):
    linkedin_url = models.URLField()
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


class Group(models.Model):
    members = models.ManyToManyField(Person, related_name='groups')
    linkedin_url = models.URLField()
    name = models.CharField(max_length=127)
    profile_picture_url = models.URLField(null=True)
