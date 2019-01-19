from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from user import views

app_name = 'user'

urlpatterns = [
    path('api/login/', obtain_jwt_token, name='login'),
    path('api/token/refresh/', refresh_jwt_token, name='refresh'),
    path('hello/', views.HelloViewAPI.as_view(), name='hello'),
    path('api/signup/', views.CreateUserViewAPI.as_view(), name='signup'),
]
