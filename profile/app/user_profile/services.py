

#from .models import Account
from django.db import transaction
from django.core.exceptions import ValidationError
from django.utils.crypto import get_random_string
from .models import Users




def create_account_number():
        """Create a new unique account number"""
        id = get_random_string(20, allowed_chars='0123456789')
        unique = False
        while not unique:
           if not Users.objects.filter(id=id):
               unique = True
           else:
               id = get_random_string(20, allowed_chars='0123456789')   
        return id
