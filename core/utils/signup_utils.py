from core.conf import HUNTER_BASE_API_ENDPOINT, HUNTER_VERIFY_EMAIL_ENDPOINT, MIN_EMAIL_VERIFICATION_SCORE

from django.conf import settings
from rest_framework import status

import requests
import clearbit


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


def collect_adv_info(email):
    """User clearbit/enrichment api and collect more info about user (using combined method)"""
    clearbit.key = settings.CLEARBIT_API_KEY

    response = clearbit.Enrichment.find(email=email, stream=True)

    if response['person'] is not None and response['person']['twitter'] is not None:
        user_twitter_handle = response['person']['twitter']['handle']
    else:
        user_twitter_handle = None

    if response['company'] is not None:
        company_name = response['company']['name']
    else:
        company_name = None

    if response['company'] is not None:
        company_location = response['company']['location']
    else:
        company_location = None

    adv_info = {
        'user_twitter_handle': user_twitter_handle,
        'company_name': company_name,
        'company_location': company_location
    }

    return adv_info
