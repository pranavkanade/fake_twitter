from bot.config import BASE_URL
import requests
from functools import reduce


class Bot:
    def __init__(self, config, url_endpoints):
        self.config = config
        self.number_of_users = config['number_of_users']
        self.max_posts_per_user = config['max_posts_per_user']
        self.max_likes_per_user = config['max_likes_per_user']
        self.url_endpoints = url_endpoints
        self.signed_up_users = None
        self.users_jwt_tokens = []
        self.detailed_users = []

    def _make_post_request(self, url_segs, payload):
        url = reduce(str.format, url_segs)
        res = requests.post(url, data=payload)
        return res.json()

    def _make_get_request(self, url_segs, header):
        url = reduce(str.format, url_segs)
        res = requests.get(url, headers=header)
        return res.json()

    def _make_patch_request(self, url_segs, header, payload):
        url = reduce(str.format, url_segs)
        res = requests.patch(url, data=payload, headers=header)
        return res.json()

    def _get_index_in_detailed_users(self, email):
        for user_index in range(len(self.detailed_users)):
            if email == self.detailed_users[user_index]['email']:
                return user_index
        return None

    def _set_token_for_email(self, email, token):
        index_in_detailed_users = \
            self._get_index_in_detailed_users(email)
        self.detailed_users[index_in_detailed_users]['token'] = token
        return

    def signup_users(self, users_signup_config):
        self.signed_up_users = users_signup_config[:self.number_of_users]
        for each_new_user in self.signed_up_users:
            user_info = self._signup_user(each_new_user)
            self.detailed_users.append(user_info)

    def _signup_user(self, new_user_config):
        # Making a POST request
        url_segments = [BASE_URL, self.url_endpoints['signup']]
        return self._make_post_request(url_segs=url_segments,
                                       payload=new_user_config)

    def login_users(self):
        for each_existing_user in self.signed_up_users:
            token_resp = self._login_user(each_existing_user)
            user_email = each_existing_user['email']
            self._set_token_for_email(email=user_email,
                                      token=token_resp['token'])

    def _login_user(self, existing_user_config):
        url_segments = [BASE_URL, self.url_endpoints['login']]
        payload = {
            'email': existing_user_config['email'],
            'password': existing_user_config['password']
        }
        return self._make_post_request(url_segs=url_segments, payload=payload)

    def renew_token_for_all(self):
        for each_existing_user in self.detailed_users:
            token_resp = self._renew_a_user_token(each_existing_user['token'])
            user_email = each_existing_user['email']
            self._set_token_for_email(email=user_email,
                                      token=token_resp['token'])

    def _renew_a_user_token(self, existing_user_details):
        url_segments = [BASE_URL, self.url_endpoints['renew_jwt_token']]
        payload = {
            'token': existing_user_details['token']
        }
        return self._make_post_request(url_segs=url_segments, payload=payload)
