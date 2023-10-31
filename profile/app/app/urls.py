from django.contrib import admin
from django.urls import path, include

from user_profile.views import *
#from rest_framework import routers
from flags.urls import flagged_path, flagged_paths, flagged_re_path, flagged_re_paths

#flagged_path('MY_FLAG', 'a-url/', view_requiring_flag, state=True), 

urlpatterns = [

    flagged_path('SEARCHS_FLAG', 'usersearch/', UsersListView.as_view(), state=False),
    flagged_path('USERS_CREATE_FLAG', 'profile1/', UsersCreate.as_view({'post': 'create'}), state=False),
    path('admin/', admin.site.urls),
    #path(r'mypage/', TemplateView.as_view(template_name='mytemplate.html')),
    flagged_path('USERS_UPDATE_FLAG', 'profile2/<str:pk>/', UsersUpdate.as_view(), state=False),
    flagged_path('USERS_DESTROY_FLAG', 'profile3/<str:pk>/', UsersDestroy.as_view(), state=False),
    flagged_path('USERSDETAIL_FLAG', 'profile4/<str:id>/', UsersDetail.as_view(), state=False),

]

