from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

from user.views import CreateUserViewAPI, ListUserViewAPI, DetailUserViewAPI

app_name = 'user'

urlpatterns = [
    path('login/', obtain_jwt_token, name='login'),
    path('token/refresh/', refresh_jwt_token, name='refresh'),
    path('signup/', CreateUserViewAPI.as_view(), name='signup'),
    path('all/', ListUserViewAPI.as_view(), name='list-users'),
    path('<int:pk>/', DetailUserViewAPI.as_view(), name='details')
]
