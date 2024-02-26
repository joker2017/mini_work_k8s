from django.db import models
from django.contrib.auth.hashers import make_password
import random

class Users(models.Model):
    """
    Represents a user in the system with custom fields and a method for hashing passwords.

    Attributes:
        id (CharField): A unique identifier for the user, manually generated.
        full_names (CharField): The full name of the user.
        username (CharField): A unique username for user identification.
        email (EmailField): The user's email address.
        password (CharField): The user's password, stored as a hashed value for security.
    """
    id = models.CharField(primary_key=True, max_length=20, blank=True, editable=False, unique=True)
    full_names = models.CharField(max_length=255)  # The full name of the user
    username = models.CharField(max_length=255)  # A unique username for the user
    email = models.EmailField(max_length=255, unique=True)  # The user's email address
    password = models.CharField(max_length=255)  # The user's hashed password

    def save(self, *args, **kwargs):
        """
        Overrides the save method to generate a unique ID and hash the password before saving.
        """
        # Generate a unique ID if it's not already set
        if not self.id:
            self.id = self.generate_unique_id_number()
        # Hash the password if it's been changed
        if 'password' in self.__dict__ or not self.pk:
            self.password = make_password(self.password)
        super(Users, self).save(*args, **kwargs)

    @staticmethod
    def generate_unique_id_number():
        """
        Generates a unique ID for the user by creating a random 20 digit string,
        ensuring it doesn't already exist in the database.
        """
        unique_id = ''.join([str(random.randint(0, 9)) for _ in range(20)])
        while Users.objects.filter(id=unique_id).exists():
            unique_id = ''.join([str(random.randint(0, 9)) for _ in range(20)])
        return unique_id

    def __str__(self):
        """
        Returns a string representation of the user, including their full names and username.
        """
        return f'{self.full_names} ({self.username})'

    class Meta:
        managed = False  # Indicates that Django should not manage this table, allowing for manual or external management
        db_table = 'user_profile_users'  # Specifies the name of the database table to use

class Account(models.Model):
    """
    Represents a user's account, including balance and a link to the corresponding user.

    Attributes:
        id (CharField): A unique identifier for the account, manually generated.
        balance (DecimalField): The financial balance of the account.
        usernameid (ForeignKey): A link to the associated user, identified by their unique ID.
    """
    id = models.CharField(primary_key=True, max_length=20, blank=True, editable=False, unique=True)
    balance = models.DecimalField(default=0, max_digits=20, decimal_places=2)  # The account's balance
    usernameid = models.ForeignKey(Users, on_delete=models.PROTECT, null=True, blank=True, related_name='accounts', default='null')

    def save(self, *args, **kwargs):
        """
        Overrides the save method to generate a unique ID before saving.
        """
        # Generate a unique ID if it's not already set
        if not self.id:
            self.id = self.generate_unique_id_number()
        super(Account, self).save(*args, **kwargs)

    @staticmethod
    def generate_unique_id_number():
        """
        Generates a unique ID for the account by creating a random 20 digit string,
        ensuring it doesn't already exist in the database.
        """
        unique_id = ''.join([str(random.randint(0, 9)) for _ in range(20)])
        while Account.objects.filter(id=unique_id).exists():
            unique_id = ''.join([str(random.randint(0, 9)) for _ in range(20)])
        return unique_id

    def __str__(self):
        """
        Returns a string representation of the account, including its ID, balance, and associated user ID.
        """
        return f"Account ID: {self.id}, Balance: {self.balance}, User ID: {self.usernameid.id}"
