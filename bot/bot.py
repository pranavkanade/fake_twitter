from bot.config import BASE_URL
import requests
from functools import reduce
import random
from pprint import pprint


class Bot:
    def __init__(self, config, url_endpoints, test_data):
        self.config = config
        self.number_of_users = config['number_of_users']
        self.max_posts_per_user = config['max_posts_per_user']
        self.max_likes_per_user = config['max_likes_per_user']
        self.url_endpoints = url_endpoints
        self.data = test_data
        self.signed_up_users = None
        self.user_index_to_num_of_posts_mapping = dict()
        self.user_index_to_created_post_id_list_mapping= dict()

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

    def _make_patch_request(self, url_segs, payload=None, header=""):
        url = reduce(str.format, url_segs)
        res = requests.patch(url, json=payload, headers=header)
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
        self.user_index_to_num_of_posts_mapping[index_in_signed_up_users] = number_of_posts

    def _get_number_of_posts_for_current_user(self, email):
        number_of_posts = random.randint(self.max_posts_per_user//2, self.max_posts_per_user)
        self._set_number_of_posts_for_signed_up_user(email, number_of_posts)
        return number_of_posts

    def signup_users(self):
        self.signed_up_users = self.data[:self.number_of_users]
        idx = 0
        for each_new_user in self.signed_up_users:
            user_info = self._signup_user(each_new_user)
            # store the id returned by the api
            self.signed_up_users[idx]['id'] = user_info['id']
            idx += 1

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
        user_index = 0
        for each_existing_user in self.signed_up_users:
            self._create_posts_with_given_user(each_existing_user, user_index)
            user_index += 1

    def _create_posts_with_given_user(self, existing_user_details, user_index):
        email = existing_user_details['email']
        token = existing_user_details['token']
        number_of_posts = self._get_number_of_posts_for_current_user(email)
        self.user_index_to_created_post_id_list_mapping[user_index] = list()
        for each_post in existing_user_details['posts'][:number_of_posts]:
            post_info = self._create_a_post(token=token, post=each_post)
            self.user_index_to_created_post_id_list_mapping[user_index].append(post_info['id'])
        print("User ( email: {} ) has created {} posts".format(email, number_of_posts))

    def _create_a_post(self, token, post):
        url_segments = [BASE_URL, self.url_endpoints['create_new_post']]
        header = self._get_valid_header_with_token(token=token)
        return self._make_post_request(url_segs=url_segments, header=header, payload=post)


    def make_users_like_post_of_other_users(self):
        # Get the users in order of number of posts they have created
        # Note: Next user who likes the post is the one with most number of posts
        list_of_users = sorted(self.user_index_to_num_of_posts_mapping.items(),
                               key=lambda item: item[1],
                               reverse=True)
        for (user_index, num_of_posts) in list_of_users:
            post_ids_user_can_like = self._get_list_of_posts_user_can_like(user_index)
            self._make_a_user_like_posts(user_index, post_ids_user_can_like)


    def _make_user_like_single_post(self, token, post_id):
        url_segments = [BASE_URL, self.url_endpoints['like_a_post'], post_id]
        header = self._get_valid_header_with_token(token=token)
        return self._make_patch_request(url_segs=url_segments, header=header)


    def _make_a_user_like_posts(self, user_index, post_ids_user_can_like):
        # Randomly choose indices of post id user is going to like
        post_id_index_to_be_liked_by_user = random.sample(range(len(post_ids_user_can_like)),
                                                          self.max_likes_per_user)
        user_token = self.signed_up_users[user_index]['token']
        for each_index in post_id_index_to_be_liked_by_user:
            self._make_user_like_single_post(user_token, post_ids_user_can_like[each_index])

    def _get_list_of_posts_user_can_like(self, user_index):
        post_ids_user_can_like = list()

        for each_key in self.user_index_to_created_post_id_list_mapping.keys():
            if each_key != user_index:
                post_ids_user_can_like.extend(self.user_index_to_created_post_id_list_mapping[each_key])
        return post_ids_user_can_like

    def get_all_posts(self):
        user_token = self.signed_up_users[0]['token']
        header = self._get_valid_header_with_token(token=user_token)
        url_segments = [BASE_URL, self.url_endpoints['get_all_posts']]
        return self._make_get_request(url_segs=url_segments, header=header)



