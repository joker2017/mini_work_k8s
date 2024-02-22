from .models3 import Account
from django.utils.crypto import get_random_string

def create_account_number():
    """
    Generate a unique account number.

    This function generates a random string of 20 digits and checks if it is unique
    by verifying against existing account numbers in the database. If the generated
    number already exists, it attempts to generate a new one until a unique number is found.

    Returns:
        str: A unique account number consisting of 20 digits.
    """
    id = get_random_string(20, allowed_chars='0123456789')
    unique = False
    while not unique:
        if not Account.objects.filter(id=id).exists():
            unique = True
        else:
            id = get_random_string(20, allowed_chars='0123456789')

    return id

