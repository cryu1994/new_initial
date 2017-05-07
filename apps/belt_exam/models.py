from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z.-]+$')
PW_REGEX = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$')

class UserManager(models.Manager):
    def register(self, PostData):
        errors = []
        if len(PostData['name']) < 1 or len(PostData['email']) < 1 or len(PostData['password']) < 1:
            errors.append("Opps! something went wrong, Check your info!")
        if not EMAIL_REGEX.match(PostData['email']):
            errors.append("Invalid Email address")
        if not NAME_REGEX.match(PostData['name']):
            errors.append("Name only can contain letters!")
        if not PW_REGEX.match(PostData['password']):
            errors.append("password not strong!")
        if PostData['conf_password'] != PostData['password']:
            errors.append("password not match!")
        if User.objects.filter(email = PostData['email']):
            errors.append("User already exist!")
        return errors
    def create_user(self, PostData):
        hashed_pw = bcrypt.hashpw(PostData['password'].encode('utf-8'), bcrypt.gensalt())
        new_user = User.objects.create(name=PostData['name'], email=PostData['email'], password = hashed_pw)
        return new_user.id
    def login(self, PostData):
        errors = []
        if len(PostData['email']) < 1 or len(PostData['password']) < 1:
            errors.append("You forgot to enter your email/password")
        if not User.objects.filter(email=PostData['email']):
            errors.append('Invlaild User!')
        else:
            if bcrypt.hashpw(PostData['password'].encode('utf-8'), User.objects.get(email=PostData['email']).password.encode('utf-8')) != User.objects.get(email=PostData['email']).password:
                errors.append('incorrect user name or password')
        return errors
        def join(self, PostData):
            User.objects.get(id=user_id).join.add(User.objects.get(id=PostData['user_id']))
            return user.id
class PlanManager(models.Manager):
    def add_plans(self, PostData):
        plan = Plan.objects.create(destination = PostData['destination'], description = PostData['description'], start = PostData['start_date'], end = PostData['end_date'], user=PostData['user'])
        plan_id = plan.id
        print plan_id
class User(models.Model):
    name = models.CharField(max_length=225)
    email = models.CharField(max_length = 225)
    password = models.CharField(max_length = 225)
    join = models.ManyToManyField("self", related_name="join")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

class Plan(models.Model):
    destination = models.CharField(max_length = 200)
    description = models.TextField(max_length = 2000)
    start = models.DateField()
    end = models.DateField()
    user = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = PlanManager()
# Create your models here.
