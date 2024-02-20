
from django.contrib import admin
from django.urls import path, include
from account.views import *
from rest_framework import routers
from rest_framework import routers
from flags.urls import flagged_path, flagged_paths, flagged_re_path, flagged_re_paths


urlpatterns = [
    path('account/admin/', admin.site.urls),
    flagged_path('ACCOUNT_LIST_FLAG', 'account/list/', AccountList.as_view({'get': 'list'}), name='account-list', state=False),
    flagged_path('ACCOUNT_CREATE_FLAG', 'account/create/', AccountCreate.as_view({'post': 'create'}), name='account-create', state=False),
    flagged_path('ACCOUNT_UPDATE_FLAG', 'account/update/<str:pk>/', AccountUpdate.as_view(), name='account-update', state=False),
    flagged_path('ACCOUNT_DESTROY_FLAG', 'account/destroy/<str:pk>/', AccountDestroy.as_view(), name='account-destroy', state=False),
    flagged_path('ACCOUNT_DETAIL_FLAG', 'account/detail/<str:usernameid>/', AccountDetail.as_view(), name='account-detail', state=False),
    

]

