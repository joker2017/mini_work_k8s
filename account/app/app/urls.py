"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from account.views import *
from rest_framework import routers
from rest_framework import routers



router = routers.SimpleRouter()
'''
router = routers.SimpleRouter()
router.register(r'account', AccountViewSet, 'accout')
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]

app_name = "accounts"
# app_name will help us do a reverse look-up latter.
urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', AccountList.as_view()),
    path('account/<str:username>/', AccountUpdate.as_view()),
    path('account/<str:username>/', AccountCreate.as_view()),
    path('account/<str:username>/', AccountDestroyView.as_view()),
]

AccountCreate   AccountUpdate      AccountDetail     AccountDestroy
'''
#router.register(r'account1', AccountCreate, 'users1')
#router = routers.SimpleRouter()
#router.register(r'account1', AccountDetail, 'detail')
#router.register(r'account2', AccountCreate, 'create')
#router.register(r'account3', AccountUpdate, 'update')
#router.register(r'account4', AccountDestroy, 'destroy')
#router.register(r'account5', AccountList, 'list')
urlpatterns = [
    path('admin/', admin.site.urls),
    path('account1/', AccountList.as_view({'get': 'list'})),
    path('account2/', AccountCreate.as_view({'post': 'create'})),
    path('account3/<str:pk>/', AccountUpdate.as_view()),
    path('account4/<str:pk>/', AccountDestroy.as_view()),
    path('account5/<str:usernameid>/', AccountDetail.as_view()),
    path('', include(router.urls)),

]

 #path('account/<str:usernameid>/', AccountUpdate.as_view({'put': 'update'})),
 #   path('account/destroy/<str:usernameid>/', AccountDestroy.as_view({'delete': 'destroy'})),
 #   path('account/detail/<str:id>/', AccountDetail.as_view({'get': 'retrieve'})),

#router = routers.SimpleRouter()
#router.register(r'profile1', AccountDetail, 'detail')
#router.register(r'profile2', AccountCreate, 'create')
#router.register(r'profile2', AccountUpdate, 'create')
#router.register(r'profile2', AccountDestroy, 'create')
#router.register(r'usersearch', UserListView, 'usersearch')
#path('', include(router.urls)),

#AccountDestroy
#AccountDetail
#AccountUpdate
#AccountCreate
#AccountList