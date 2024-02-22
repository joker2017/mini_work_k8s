from django.utils.crypto import get_random_string
from .models import Users


def create_account_number():
    """
    Generates a new unique account number.

    This function generates a random string of 20 digits, ensuring that
    it is unique by checking against existing account numbers in the Users model.
    If a generated number already exists, it repeats the process until a unique number is found.
    """

    # Initialize a unique identifier with a random 20-digit string
    id = get_random_string(20, allowed_chars='0123456789')
    unique = False  # Flag to check uniqueness

    while not unique:
        # Check if the generated id exists in the Users model
        if not Users.objects.filter(id=id).exists():
            # If not exists, the id is unique
            unique = True
        else:
            # If exists, generate a new id and check again
            id = get_random_string(20, allowed_chars='0123456789')

    # Return the unique account number
    return id
