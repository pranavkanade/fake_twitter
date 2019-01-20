import requests
from django.conf import settings
from core.conf import HUNTER_BASE_API_ENDPOINT, HUNTER_VERIFY_EMAIL_ENDPOINT, MIN_EMAIL_VERIFICATION_SCORE
from rest_framework import status


def verify_email(email):
    """Verify if email is reachable using hunter.io"""
    url = HUNTER_BASE_API_ENDPOINT.format(HUNTER_VERIFY_EMAIL_ENDPOINT)
    args = {
        'email': email,
        'api_key': settings.HUNTER_API_KEY
    }
    res = requests.get(url, params=args)

    try:
        data = res.json()['data']
        # this score is the only quantifiable thing in the response
        score = data['score']
    except KeyError:
        # if necessary further processing can be done using res.json()['errors']
        error = res.json()['errors'][0]
        return False, error['code'], error['details']
    else:
        if score >= MIN_EMAIL_VERIFICATION_SCORE:
            return True, status.HTTP_200_OK, None
        else:
            error_details = "Our system cannot test the validity of the provided email address." \
                            " Please provide different email address."
            return False, status.HTTP_400_BAD_REQUEST, error_details

