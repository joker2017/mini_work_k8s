
from django.contrib import admin
from django.urls import path, include
from account.views import *
from rest_framework import routers
from rest_framework import routers
from flags.urls import flagged_path, flagged_paths, flagged_re_path, flagged_re_paths


urlpatterns = [
    path('admin/', admin.site.urls),
    flagged_path('ACCOUNT_LIST_FLAG', 'list/', AccountList.as_view({'get': 'list'}), state=False),
    flagged_path('ACCOUNT_CREATE_FLAG', 'create/', AccountCreate.as_view({'post': 'create'}), state=False),
    flagged_path('ACCOUNT_UPDATE_FLAG', 'update/<str:pk>/', AccountUpdate.as_view(), state=False),
    flagged_path('ACCOUNT_DESTROY_FLAG', 'destroy/<str:pk>/', AccountDestroy.as_view(), state=False),
    flagged_path('ACCOUNT_DETAIL_FLAG', 'detail/<str:usernameid>/', AccountDetail.as_view(), state=False),
    

]

