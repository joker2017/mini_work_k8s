from django.contrib import admin
from django.urls import path
from account.views import *
from flags.urls import flagged_path, flagged_paths, flagged_re_path, flagged_re_paths

# URL configuration for the account application.
# This configuration includes paths for listing, creating, updating, destroying,
# and retrieving the details of accounts. Each path is associated with a specific
# view that handles the request.
# The `flagged_path` function is used to conditionally enable or disable these
# endpoints based on the state of feature flags defined in the settings.

urlpatterns = [
    # Admin panel URL.
    path('account/admin/', admin.site.urls),

    # List all accounts. Enabled/Disabled based on ACCOUNT_LIST_FLAG.
    flagged_path('ACCOUNT_LIST_FLAG', 'account/list/', AccountListView.as_view(), state=False),

    # Create a new account. Enabled/Disabled based on ACCOUNT_CREATE_FLAG.
    flagged_path('ACCOUNT_CREATE_FLAG', 'account/create/', AccountCreate.as_view(), state=False),

    # Update an existing account. Enabled/Disabled based on ACCOUNT_UPDATE_FLAG.
    flagged_path('ACCOUNT_UPDATE_FLAG', 'account/update/<str:pk>/', AccountUpdate.as_view(), state=False),

    # Destroy an existing account. Enabled/Disabled based on ACCOUNT_DESTROY_FLAG.
   # flagged_path('ACCOUNT_DESTROY_FLAG', 'account/destroy/<str:pk>/', AccountDestroy.as_view(), state=False),
    flagged_path('ACCOUNT_DESTROY_FLAG', 'account/destroy/<str:pk>/', AccountDestroy.as_view(), state=False),
    # Retrieve the details of a specific account. Enabled/Disabled based on ACCOUNT_DETAIL_FLAG.
    flagged_path('ACCOUNT_DETAIL_FLAG', 'account/detail/<str:pk>/', AccountDetail.as_view(), state=False),
]

