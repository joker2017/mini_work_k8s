from django.db import models
from hashlib import sha256

class Users(models.Model):
    """
    Represents a user in the system.

    Attributes:
    - id: A unique identifier for the user.
    - full_names: The full name of the user.
    - username: The user's username, used for login and identification.
    - email: The user's email address.
    - password: The user's password, stored in a hashed format for security.
    """
    id = models.CharField(primary_key=True, max_length=20, blank=True, editable=False, unique=True)
    full_names = models.CharField(max_length=255)  # Full names
    username = models.CharField(max_length=255)  # Username
    email = models.EmailField(max_length=255)  # Email
    password = models.CharField(max_length=255)  # Password
    USERNAME_FIELD = "username"

    def save(self, *args, **kwargs):
        """
        Overrides the save method to hash the password before saving the user.
        """
        if self.password:
            self.password = sha256(self.password.encode('utf-8')).hexdigest()
        super().save(*args, **kwargs)

    class Meta:
        managed = False  # Indicates that Django should not manage the table creation for this model
        db_table = 'user_profile_users'  # Specifies the name of the database table

class Account(models.Model):
    """
    Represents an account associated with a user.

    Attributes:
    - id: A unique identifier for the account.
    - balance: The current balance of the account.
    - usernameid: A foreign key linking to the associated user.
    """
    id = models.CharField(primary_key=True, max_length=20, blank=True, editable=False, unique=True)
    balance = models.DecimalField(default=0, max_digits=20, decimal_places=2)
    usernameid = models.ForeignKey('Users', default='null', on_delete=models.PROTECT, null=True, related_name='users', blank=True)

    def __str__(self):
        """
        Returns a string representation of the account, useful for debugging purposes.
        """
        return f'Account {self.id} with balance {self.balance}'
