from django.contrib import admin
from django.urls import path, include
from user_profile.views import *
from flags.urls import flagged_path, flagged_paths, flagged_re_path, flagged_re_paths



urlpatterns = [

    flagged_path('SEARCHS_FLAG', 'profile/usersearch/', UsersListView.as_view(), state=False),
    flagged_path('USERS_CREATE_FLAG', 'profile/create/', UsersCreate.as_view({'post': 'create'}), state=False),
    path('profile/admin/', admin.site.urls),
    flagged_path('USERS_UPDATE_FLAG', 'profile/update/<str:pk>/', UsersUpdate.as_view(), state=False),
    flagged_path('USERS_DESTROY_FLAG', 'profile/destroy/<str:pk>/', UsersDestroy.as_view(), state=False),
    flagged_path('USERSDETAIL_FLAG', 'profile/detail/<str:id>/', UsersDetail.as_view(), state=False),

]

