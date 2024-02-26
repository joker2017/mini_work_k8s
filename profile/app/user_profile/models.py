from django.db import models
from django.contrib.auth.hashers import make_password
import random

class Users(models.Model):
    """
    Represents a user in the system with custom fields including hashed password.

    Attributes:
        id (str): A unique identifier for the user. It's a 20-character long string.
        full_names (str): The full name of the user.
        username (str): A unique username for the user.
        email (str): The user's email address.
        password (str): The user's password, stored in a hashed format for security.
    """
    id = models.CharField(
        primary_key=True,
        max_length=20,
        blank=True,
        editable=False,
        unique=True,
    )
    full_names = models.CharField(max_length=255)  # User's full name
    username = models.CharField(max_length=255)  # Unique username for the user
    email = models.EmailField(max_length=255, unique=True)  # User's email address
    password = models.CharField(max_length=255)  # Hashed password for security

    def save(self, *args, **kwargs):
        """
        Overrides the save method to ensure a unique ID is generated for new users
        and passwords are hashed before saving.
        """
        # Generate a unique ID if not set
        if not self.id:
            self.id = self.generate_unique_id_number()
        # Hash password before saving if it's been modified
        if 'password' in self.__dict__ or not self.pk:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    @staticmethod
    def generate_unique_id_number():
        """
        Generates a unique ID for the user.

        Returns:
            str: A unique 20-digit ID.
        """
        unique_id = ''.join([str(random.randint(0, 9)) for _ in range(20)])
        while Users.objects.filter(id=unique_id).exists():
            unique_id = ''.join([str(random.randint(0, 9)) for _ in range(20)])
        return unique_id

    def __str__(self):
        """
        String representation of the Users model.

        Returns:
            str: The full name and username of the user.
        """
        return f'{self.full_names} ({self.username})'


class Account(models.Model):
    """
    Represents a user's account with a balance and link to the user.

    Attributes:
        id (str): A unique identifier for the account, similar to the Users model.
        balance (Decimal): The financial balance of the account.
        usernameid (ForeignKey): A reference to the associated user.
    """
    id = models.CharField(
        primary_key=True,
        max_length=20,
        blank=True,
        editable=False,
        unique=True,
    )
    balance = models.DecimalField(
        default=0,
        max_digits=20,
        decimal_places=2
    )
    usernameid = models.ForeignKey(
        'Users',
        default='null',
        on_delete=models.PROTECT,
        null=True,
        related_name='accounts',
        blank=True
    )

    def save(self, *args, **kwargs):
        """
        Overrides the save method to ensure a unique ID is generated for new accounts.
        """
        # Generate a unique ID if not set
        if not self.id:
            self.id = self.generate_unique_id_number()
        super().save(*args, **kwargs)

    @staticmethod
    def generate_unique_id_number():
        """
        Generates a unique ID for the account.

        Returns:
            str: A unique 20-digit ID.
        """
        unique_id = ''.join([str(random.randint(0, 9)) for _ in range(20)])
        while Account.objects.filter(id=unique_id).exists():
            unique_id = ''.join([str(random.randint(0, 9)) for _ in range(20)])
        return unique_id

    def __str__(self):
        """
        String representation of the Account model.

        Returns:
            str: A summary of the account including ID, balance, and associated user.
        """
        return f"Account ID: {self.id}, Balance: {self.balance}, User: {self.usernameid.username}"

    class Meta:
        managed = False  # Indicates that Django should not manage table creation for this model
        db_table = 'account_account'  # Specifies the name of the database table
