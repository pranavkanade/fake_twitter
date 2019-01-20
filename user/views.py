from django.contrib.auth import get_user_model
from django.http.response import JsonResponse
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated

from core.models import UserAdvInfo
from core.utils.signup_utils import verify_email, collect_adv_info
from user.serializers import UserAdvInfoSerializer, UserDetailSerializer, UserSerializer


class DetailUserViewAPI(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserDetailSerializer
    queryset = get_user_model().objects.all()


class ListUserViewAPI(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()


class CreateUserAdvInfo(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserAdvInfoSerializer


# can also use ListCreateAPIView to get both GET and POST here
class CreateUserViewAPI(generics.CreateAPIView):
    """Create new user using api"""
    permission_classes = (AllowAny,)
    serializer_class = UserDetailSerializer

    def perform_create(self, serializer):
        new_user_email = self.request.data['email']
        adv_info_payload = collect_adv_info(new_user_email)
        adv_info = UserAdvInfo.objects.create(**adv_info_payload)
        serializer.save(adv_info=adv_info)

    def post(self, request, *args, **kwargs):
        new_user_email = request.data['email']

        # In case of valid email address: primary_ret_code = 200 & primary_error = None
        is_email_valid, primary_ret_code, primary_error_details = verify_email(email=new_user_email)
        if is_email_valid:
            # Score is more than min
            return self.create(request, *args, **kwargs)
        else:
            return self.verify_email_error_handler(ret_code=primary_ret_code, error_details=primary_error_details)

    def verify_email_error_handler(self, ret_code, error_details):
        if ret_code == status.HTTP_401_UNAUTHORIZED:
            # This means there is problem with API key
            # TODO: Add this to logging
            res = {
                'error': {
                    'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'details': "Internal Server Error! Please try again, after some time."
                }
            }
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        else:
            # @Here means -
            # Either email is not valid - got error from hunter.io other than 401 (above)
            # OR
            # Did not encounter error with the verification API but, the score is low
            res = {
                'error': {
                    'code': status.HTTP_400_BAD_REQUEST,
                    'details': error_details
                }
            }
            status_code = status.HTTP_400_BAD_REQUEST

        return JsonResponse(data=res, status=status_code)
