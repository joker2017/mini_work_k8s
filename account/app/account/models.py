from django.db import models
from django.conf import settings

import os
from django.db import transaction
import random

from hashlib import sha256

from django.utils.text import slugify
import uuid

from django.utils.crypto import get_random_string

from rest_framework.response import Response
from rest_framework import status
from django.db import IntegrityError

class Users(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length = 20,
        blank=True,
        editable=False,
        unique=True,
                        )
    full_names = models.CharField(max_length=255)  #Full_names
    username = models.CharField(max_length=255)  #username
    email = models.EmailField(max_length=255)   #email
    password = models.CharField(max_length=255)  # password
    USERNAME_FIELD = "username"


    def save(self, *args, **kwargs):
      if self.password:
        self.password = sha256(self.password.encode('utf-8')).hexdigest()
      super().save(*args, **kwargs)

    class Meta:
        managed = False
        db_table = 'user_profile_users'





class Account(models.Model):
    id = models.CharField(
        #max_digits=20, 
        #decimal_places=0,
    #models.CharField(
        #default = get_random_string(20, allowed_chars='0123456789'),
        primary_key=True,
        max_length = 20,
        blank=True,
        editable=False,
        unique=True,
                        )
    
    balance = models.DecimalField(
        default=0,
        max_digits=20,
        decimal_places=2
    )
    usernameid = models.ForeignKey('Users', default='null', on_delete=models.PROTECT, null=True, related_name='users', blank=True)

    def __str__(self):
       return '__all__'

