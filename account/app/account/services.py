

from .models import Account
from django.db import transaction
from django.core.exceptions import ValidationError
from django.utils.crypto import get_random_string





def create_account_number():
        """Create a new unique account number"""
        print("начинаю считать")
        id = get_random_string(20, allowed_chars='0123456789')
        print("номер аккаунта !!!!!!!!!!!!!!!!!!!", id)
        unique = False
        while not unique:
           if not Account.objects.filter(id=id).exists():
               print(", не нашли такой же аккаунт")
               unique = True
           else:
               print("ой, аккаунт повторился")
               id = get_random_string(20, allowed_chars='0123456789')
        print("вот что в итоге вышло из функции", id)       
        return id


'''


def make_interest():
    accounts = Account.objects.all()
    for account in accounts:
        with transaction.atomic():
            pr = 0.08 / 12
            balance = float(account.balance)
            interest = balance * pr
            balance += interest
            account.balance = balance
            Interest.objects.create(
                account=account,
                amount=interest
            )
            account.save()
'''