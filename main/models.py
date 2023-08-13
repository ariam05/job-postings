from django.db import models

# Create your models here.
from django.db import models
import re

# Create your models here.
class UserManager(models.Manager):
    def user_validator(self, form_data):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(form_data['f_name']) < 2 or not form_data['f_name'].isalpha():
            errors['f_name'] = "First name must be at least 2 characters and/or letters only!"
        if len(form_data['l_name']) < 2 or not form_data['l_name'].isalpha():
            errors['l_name'] = "Last name must be at least 2 characters and/or letters only!"
        if not EMAIL_REGEX.match(form_data['email']):
            errors['email'] = "Email doesn't look right!"
        if len(form_data['email']) < 6:
            errors['email_length'] = "Email is too short! Email needs to be at least 6 characters" #keys need to be different, can make up any name
        if len(form_data['password']) < 8:
            errors['password'] = "Password must be at least 8 characters!" 
        if form_data['password'] != form_data['confirm_password']:
            errors['confirm_password'] = "Passwords don't match! Try again!"
        return errors  
    def login_validator(self, form_data):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(form_data['email']):
            errors['email'] = "Email doesn't look right!"
        if len(form_data['email']) < 6:
            errors['email_length'] = "Email is too short! Email needs to be at least 6 characters"
        return errors
    def create_job_validator(self, form_data):
        errors = {}
        if len(form_data['title']) < 3:
            errors['title'] = "A Job must consist of at least 3 characters!"
        if len(form_data['description']) < 3:
            errors['description'] = "Description must consist of at least 3 characters!"
        if len(form_data['location']) < 3:
            errors['location'] = "A valid location must be provided!"
        return errors
        

class User(models.Model):
    f_name = models.CharField(max_length=255)
    l_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    objects = UserManager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Job(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    submitted_by = models.ForeignKey(User, related_name = 'submitted_jobs', on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)