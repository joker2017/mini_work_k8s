# models.py
from rest_framework import serializers
from .models import Users, Account
import random
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def generate_unique_id(self):
        unique_id = ''.join([str(random.randint(0, 9)) for _ in range(20)])
        while self.model.objects.filter(id=unique_id).exists():
            unique_id = ''.join([str(random.randint(0, 9)) for _ in range(20)])
        return unique_id

class Users(AbstractBaseUser):
    id = models.CharField(primary_key=True, max_length=20, blank=True, editable=False, unique=True)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)
    full_names = models.CharField(max_length=100)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = self.objects.generate_unique_id()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'

class Account(models.Model):
    id = models.CharField(primary_key=True, max_length=20, blank=True, editable=False, unique=True)
    balance = models.DecimalField(default=0, max_digits=20, decimal_places=2)
    user = models.ForeignKey(Users, on_delete=models.PROTECT, null=True, related_name='accounts', blank=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = Account.generate_unique_id()
        super(Account, self).save(*args, **kwargs)

    @staticmethod
    def generate_unique_id():
        unique_id = ''.join([str(random.randint(0, 9)) for _ in range(20)])
        while Account.objects.filter(id=unique_id).exists():
            unique_id = ''.join([str(random.randint(0, 9)) for _ in range(20)])
        return unique_id

    def __str__(self):
        return f'Account {self.id} with balance {self.balance}'

    class Meta:
        managed = False  # Indicates that Django should not manage the table creation for this model
        db_table = 'user_profile_users'  # Specifies the name of the database table