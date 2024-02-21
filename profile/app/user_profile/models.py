from django.db import models
from hashlib import sha256
import uuid
#from polymorphic.models import PolymorphicModel
from rest_framework.response import Response
from rest_framework import status
from django.db.models.deletion import ProtectedError
from django.db import IntegrityError
class Users(models.Model):
    #https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Models
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4)   #uuid.uuid4().hex   default=uuid.uuid4
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
  
    #https://dvmn.org/encyclopedia/django/dont-overridde-common-model-methods/   
    def save(self, *args, **kwargs):
      if self.password:
         self.password = sha256(self.password.encode('utf-8')).hexdigest()
      super().save(*args, **kwargs)



    def __str__(self):
        return f'{self.full_names} {self.username}'

    class Meta:
        app_label = 'user_profile'



#class Meta: app_label = 'user_profile' добавлен так как не определялась модельь притестировании

class Account(models.Model):
    id = models.CharField(
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

    class Meta:
        managed = False
        db_table = 'account_account'

