from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from user import views

app_name = 'user'

urlpatterns = [
    path('login/', obtain_jwt_token, name='login'),
    path('token/refresh/', refresh_jwt_token, name='refresh'),
    path('signup/', views.CreateUserViewAPI.as_view(), name='signup'),
]
