from bot.config import BASE_URL
import requests
from functools import reduce
from random import randint


class Bot:
    def __init__(self, config, url_endpoints, test_data):
        self.config = config
        self.number_of_users = config['number_of_users']
        self.max_posts_per_user = config['max_posts_per_user']
        self.max_likes_per_user = config['max_likes_per_user']
        self.url_endpoints = url_endpoints
        self.data = test_data
        self.signed_up_users = None
        self.user_to_num_of_post_mapping = dict()

    def _get_valid_header_with_token(self, token):
        header =  {
            "Authorization": " ".join(["JWT", token])
        }
        return header

    def _make_post_request(self, url_segs, payload=None, header={}):
        url = reduce(str.format, url_segs)
        res = requests.post(url, json=payload, headers=header)
        return res.json()

    def _make_get_request(self, url_segs, header):
        url = reduce(str.format, url_segs)
        res = requests.get(url, headers=header)
        return res.json()

    def _make_patch_request(self, url_segs, payload, header):
        url = reduce(str.format, url_segs)
        res = requests.patch(url, data=payload, headers=header)
        return res.json()

    def _get_index_in_signed_up_users(self, email):
        for user_index in range(len(self.signed_up_users)):
            if email == self.signed_up_users[user_index]['email']:
                return user_index
        return None

    def _set_token_in_signed_up_users_for_email(self, email, token):
        index_in_signed_up_users = \
            self._get_index_in_signed_up_users(email)
        self.signed_up_users[index_in_signed_up_users]['token'] = token
        return

    def _set_number_of_posts_for_signed_up_user(self, email, number_of_posts):
        index_in_signed_up_users = self._get_index_in_signed_up_users(email)
        self.signed_up_users[index_in_signed_up_users]['number_of_posts'] = number_of_posts
        self.user_to_num_of_post_mapping[email] = number_of_posts

    def _get_number_of_posts_for_current_user(self, email):
        number_of_posts = randint(self.max_posts_per_user//2, self.max_posts_per_user)
        self._set_number_of_posts_for_signed_up_user(email, number_of_posts)
        return number_of_posts

    def signup_users(self):
        self.signed_up_users = self.data[:self.number_of_users]
        for each_new_user in self.signed_up_users:
            user_info = self._signup_user(each_new_user)

    def _signup_user(self, new_user):
        # Making a POST request
        url_segments = [BASE_URL, self.url_endpoints['signup']]
        payload = {
            'email': new_user['email'],
            'username': new_user['username'],
            'password': new_user['password']
        }
        return self._make_post_request(url_segs=url_segments,
                                       payload=payload)

    def login_users(self):
        for each_existing_user in self.signed_up_users:
            token_resp = self._login_user(each_existing_user)
            user_email = each_existing_user['email']
            self._set_token_in_signed_up_users_for_email(email=user_email,
                                                         token=token_resp['token'])

    def _login_user(self, existing_user_config):
        url_segments = [BASE_URL, self.url_endpoints['login']]
        payload = {
            'email': existing_user_config['email'],
            'password': existing_user_config['password']
        }
        return self._make_post_request(url_segs=url_segments, payload=payload)

    def renew_token_for_all(self):
        for each_existing_user in self.signed_up_users:
            token_resp = self._renew_a_user_token(each_existing_user['token'])
            user_email = each_existing_user['email']
            self._set_token_in_signed_up_users_for_email(email=user_email,
                                                         token=token_resp['token'])

    def _renew_a_user_token(self, existing_user_details):
        url_segments = [BASE_URL, self.url_endpoints['renew_jwt_token']]
        payload = {
            'token': existing_user_details['token']
        }
        return self._make_post_request(url_segs=url_segments, payload=payload)

    def create_posts(self):
        for each_existing_user in self.signed_up_users:
            self._create_posts_with_given_user(each_existing_user)

    def _create_posts_with_given_user(self, existing_user_details):
        email = existing_user_details['email']
        token = existing_user_details['token']
        number_of_posts = self._get_number_of_posts_for_current_user(email)
        for each_post in existing_user_details['posts'][:number_of_posts]:
            self._create_a_post(token=token, post=each_post)
        print("User ( email: {} ) has created {} posts".format(email, number_of_posts))

    def _create_a_post(self, token, post):
        url_segments = [BASE_URL, self.url_endpoints['create_new_post']]
        header = self._get_valid_header_with_token(token=token)
        return self._make_post_request(url_segs=url_segments, header=header, payload=post)
