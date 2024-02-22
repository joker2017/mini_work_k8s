from django.contrib import admin
from django.urls import path
from user_profile.views import *
from flags.urls import flagged_path, flagged_paths, flagged_re_path, flagged_re_paths

# URL configuration for the user_profile application.
# This configuration is designed to control access to various user profile management
# functionalities such as searching, creating, updating, destroying, and viewing details
# of user profiles. The use of feature flags through `flagged_path` allows for flexible
# enabling or disabling of these functionalities based on the application's requirements.

urlpatterns = [
    # Admin panel URL for the user_profile application.
    path('profile/admin/', admin.site.urls),

    # Search for user profiles. Enabled/Disabled based on SEARCHS_FLAG.
    flagged_path('SEARCHS_FLAG', 'profile/usersearch/', UsersListView.as_view(), state=False),

    # Create a new user profile. Enabled/Disabled based on USERS_CREATE_FLAG.
    flagged_path('USERS_CREATE_FLAG', 'profile/create/', UsersCreate.as_view({'post': 'create'}), state=False),

    # Update an existing user profile. Enabled/Disabled based on USERS_UPDATE_FLAG.
    flagged_path('USERS_UPDATE_FLAG', 'profile/update/<str:pk>/', UsersUpdate.as_view(), state=False),

    # Delete an existing user profile. Enabled/Disabled based on USERS_DESTROY_FLAG.
    flagged_path('USERS_DESTROY_FLAG', 'profile/destroy/<str:pk>/', UsersDestroy.as_view(), state=False),

    # View details of a specific user profile. Enabled/Disabled based on USERSDETAIL_FLAG.
    flagged_path('USERSDETAIL_FLAG', 'profile/detail/<str:id>/', UsersDetail.as_view(), state=False),
]
