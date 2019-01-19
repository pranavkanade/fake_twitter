from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from user import views

app_name = 'user'

urlpatterns = [
    path('api/token/', obtain_jwt_token, name='get-jwt-token'),
    path('api/token/refresh/', refresh_jwt_token, name='refresh-jwt-token'),
    path('hello/', views.HelloViewAPI.as_view(), name='hello'),
]
