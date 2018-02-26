# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import bcrypt
from django.db import models
import re
from datetime import datetime, date

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9+-_.]+\.[a-zA-Z]+$')

# Create your models here.
class UserManager(models.Manager):
    def registration(self, postData):
        errors= []
        if len(postData['first_name']) < 1:
            errors.append("Must input a first name")
        elif len(postData["first_name"]) < 3:
            errors.append("first name must be at least 3 characters")
        if len(postData["last_name"]) <1:
            errors.append("Must input a last name")
        elif len(postData["last_name"]) < 3:
            errors.append("last name must be at least 3 characters")
        if len(postData["email"]) < 1:
            errors.append("Must input an email")
        elif not EMAIL_REGEX.match(postData["email"]):
            errors.append("Invalid email")
        if len(postData["password"]) < 1:
            errors.append("Must set a password")
        elif len(postData["password"]) < 8:
            errors.append("Password must be no fewer then 8 characters")
        if len(postData["confirm"]) < 1:
            errors.append("Must confirm the password")
        elif postData["confirm"] != postData["password"]:
            errors.append("Confirm must match the password")
        if len(errors) > 0:
            return (False, errors)
        else:
            user = User.objects.create(
                first_name= postData["first_name"],
                last_name=postData["last_name"],
                email=postData["email"].lower(),
                password=bcrypt.hashpw(postData["password"].encode(), bcrypt.gensalt())
            )
            return (True, user)
    def login(self, postData):
        response = {
            "errors": [],
            "is_valid": True,
            "user": None
        }
        if len(postData["login_email"]) <1:
            response["errors"].append("Input email")
        elif not EMAIL_REGEX.match(postData["login_email"]):
            response["errors"].append("invalid email")
        else:
            match = User.objects.filter(email=postData["login_email"])
            if len(match) < 1:
                response["errors"].append("email does not exist")
        if len(postData["login_password"]) < 1:
            response["errors"].append("input password")
        if len(response["errors"]) <1:
            user = match[0]
            if bcrypt.checkpw(postData["login_password"].encode(), user.password.encode()):
                response["user"]=user
            else:
                response["errors"].append("password is incorrect")
        if len(response["errors"]) > 0:
            response["is_valid"] = False
        return response

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = UserManager()

class TripManager(models.Manager):
    def tripValidation(self, postData, id):
        errors = []
        if len(postData["destination"]) < 1:
            errors.append("Must enter a destination")
        if len(postData["description"]) < 1:
            errors.append("Must enter a description")
        if str(date.today()) > str(postData['start']):
            errors.append("Start time can not be in the past.")
        if str(date.today()) > postData['end']:
            errors.append("End date must be in the future")
        if postData['start'] > postData['end']:
            errors.append("Travel Date From must be after Travel Date To")
        if len(errors) > 0:
            return (False, errors)
        else:
            plan= Trip.objects.create(
                destination=postData['destination'],
                description=postData['description'],
                start=postData['start'],end=postData['end'],
                creator= User.objects.get(id=id)
            )
            return (True, plan)
    def join(self,trip_id,id):
        if len(User.objects.filter(id=id).filter(joining=trip_id)) > 0:
            response = {
            "error": "You've already joined this trip"
            }
            return response
        else:
            a = Trip.objects.get(id=trip_id)
            b = User.objects.get(id=id)
            a.joiners.add(b)
            return {}

class Trip(models.Model):
    destination = models.CharField(max_length=255)
    description = models.TextField()
    start = models.DateField()
    end = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User)
    joiners = models.ManyToManyField(User, related_name="joining")
    objects = TripManager()
