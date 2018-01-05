# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import re
import bcrypt

EMAIL_REGEX = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
ALIAS_REGEX = re.compile(r"(^[a-zA-Z0-9_.+-]+$)")
NAME_REGEX = re.compile(r"(^[a-zA-Z /-]+$)") ##allows for hyphenated names and full first and last.  allowing a space is janky


# Create your models here.
class UserManager(models.Manager):
    def createUser(self, postData):
        newUser = self.create(
            name = postData['name'],
            alias = postData['alias'],
            email = postData['email'],
            password = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
        )
        return newUser

    def validateReg(self, postData):
        results = {'status': True, 'errors':[]}
        #### Name Validation
        if len(postData['name']) < 2:
            results['status'] = False
            results['errors'].append('Names must be more than 2 characters')
        if re.match(NAME_REGEX, postData['name']) == None:
            results['status'] = False
            results['errors'].append('Names may not contain special characters except spaces and dashes')

        #### Alias Validation
        if len(postData['alias']) < 2:
            results['status'] = False
            results['errors'].append('Aliases must be more than 2 characters')
        if re.match(ALIAS_REGEX, postData['alias']) == None:
            results['status'] = False
            results['errors'].append('Aliases not contain special characters except: _ . + -')
        if len(self.filter(alias= postData['email'])) > 0:
            results['status'] = False
            results['errors'].append('Alias already in use')

        #### Email Validation
        if re.match(EMAIL_REGEX, postData['email'])==None:
            results['status'] = False
            results['errors'].append('Invalid Email')
        if len(self.filter(email = postData['email'])) > 0:
            results['status'] = False
            results['errors'].append('Email already in use')

        #### Password Validation
        if len(postData['password']) < 8:
            results['status'] = False
            results['errors'].append('Passwords must be 8 or more characters')
        if postData['password'] != postData['c_password']:
            results['status'] = False
            results['errors'].append('Passwords do not match')

        return results
    
    def validateLogin(self, postData):
        results = {'status': True, 'errors':[], 'user': None}

        #### Email Validation
        if re.match(EMAIL_REGEX, postData['email'])==None:
            results['status'] = False
            results['errors'].append('Invalid Email')
        else:
            if len(self.filter(email = postData['email'])) < 1:
                results['status'] = False
                results['errors'].append('Incorrect Email or Password')
            else:
                results['user'] = self.filter(email = postData['email'])[0]
                if not bcrypt.checkpw(postData['password'].encode(), results['user'].password.encode()):
                    results['status'] = False
                    results['errors'].append('Incorrect Email or Password')

        return results

class User(models.Model):
    name = models.CharField(max_length=500)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    objects = UserManager()
