# test_services.py
import unittest
from unittest.mock import patch
from ..services import create_account_number


import pytest
from unittest.mock import patch


@pytest.mark.django_db
def test_create_account_number():
    with patch('account.app.account.models.Account.objects.filter') as mock_filter:
        mock_filter.return_value.exists.return_value = False

        account_number = create_account_number()

        assert len(account_number) == 20
        assert account_number.isdigit()
        mock_filter.assert_called()



