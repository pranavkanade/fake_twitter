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
        # { user_id : user_index in signed up users }
        self.user_id_to_user_index_mapping = dict()
        self.user_index_to_number_of_posts_mapping = dict()
        self.user_index_to_created_post_id_list_mapping = dict()
        self.user_index_to_num_of_posts_with_no_likes_mapping = dict()
        self.post_id_to_user_index_mapping = dict()

    """
    @params: token - jwt token
    """
    def _get_valid_header_with_token(self, token):
        header =  {
            "Authorization": " ".join(["JWT", token])
        }
        return header

    def _make_post_request(self, url_segs, payload=None, header=None):
        url = reduce(str.format, url_segs)
        res = requests.post(url, json=payload, headers=header)
        return res.json()

    def _make_get_request(self, url_segs, header):
        url = reduce(str.format, url_segs)
        res = requests.get(url, headers=header)
        return res.json()

    def _make_patch_request(self, url_segs, payload=None, header=None):
        url = reduce(str.format, url_segs)
        res = requests.patch(url, json=payload, headers=header)
        return res.json()

    # Functions for signed up users

    def _get_user_index_in_signed_up_users(self, email):
        for user_index in range(len(self.signed_up_users)):
            if email == self.signed_up_users[user_index]['email']:
                return user_index
        return None

    def _set_user_id_for_signed_up_user(self, user_index, id):
        self.signed_up_users[user_index]['id'] = id
        self.user_id_to_user_index_mapping[id] = user_index

    def _set_token_for_signed_up_user(self, user_index, token):
        self.signed_up_users[user_index]['token'] = token

    def _set_number_of_posts_for_signed_up_user(self, user_index, number_of_posts):
        self.signed_up_users[user_index]['number_of_posts'] = number_of_posts
        self._map_number_of_posts_to_creators_user_id(user_index,
                                                      number_of_posts)

    def _set_post_ids_list_for_signed_up_user(self, user_index, post_ids_list):
        self.signed_up_users[user_index]['post_ids_list'] = post_ids_list
        self._map_post_id_list_to_creators_user_id(user_index, post_ids_list)

    def _map_post_id_list_to_creators_user_id(self, user_index, post_ids_list):
        self.user_index_to_created_post_id_list_mapping[user_index] = post_ids_list

    def _map_number_of_posts_to_creators_user_id(self, user_index, number_of_posts):
        self.user_index_to_number_of_posts_mapping[user_index] = number_of_posts

    """
    As per requirement:
        User can create any number of posts between 0 and Max num of post
    """
    def _get_number_of_posts_for_current_user(self, user_index):
        number_of_posts = random.randint(0, self.max_posts_per_user)
        self._set_number_of_posts_for_signed_up_user(user_index, number_of_posts)
        return number_of_posts

    """
    Function to create users, given in ./data/user_test_data.json
    """
    def signup_users(self):
        self.signed_up_users = self.data[:self.number_of_users]
        for user_index, each_new_user in enumerate(self.signed_up_users):
            user_info = self._signup_user(each_new_user)
            # store the id returned by the api
            self._set_user_id_for_signed_up_user(user_index, user_info['id'])

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

    """
    Function to log the user in and get the jwt auth token
    """
    def login_users(self):
        for user_index, each_existing_user in enumerate(self.signed_up_users):
            token_resp = self._login_user(each_existing_user)
            self._set_token_for_signed_up_user(user_index=user_index,
                                               token=token_resp['token'])

    def _login_user(self, existing_user_config):
        url_segments = [BASE_URL, self.url_endpoints['login']]
        payload = {
            'email': existing_user_config['email'],
            'password': existing_user_config['password']
        }
        return self._make_post_request(url_segs=url_segments, payload=payload)

    """
    User might have to refresh his/her token after it expires
    """
    def renew_token_for_all(self):
        for user_index, each_existing_user in enumerate(self.signed_up_users):
            token_resp = self._renew_a_user_token(each_existing_user['token'])
            self._set_token_for_signed_up_user(user_index=user_index,
                                               token=token_resp['token'])

    def _renew_a_user_token(self, existing_user_details):
        url_segments = [BASE_URL, self.url_endpoints['renew_jwt_token']]
        payload = {
            'token': existing_user_details['token']
        }
        return self._make_post_request(url_segs=url_segments, payload=payload)

    """
    Make user create new posts.
    NOTE: number of posts is selected at random
    """
    def make_users_create_posts(self):
        for user_index, each_existing_user in enumerate(self.signed_up_users):
            self._make_a_user_create_multiple_posts(each_existing_user, user_index)

    def _make_a_user_create_multiple_posts(self, existing_user_details, user_index):
        email = existing_user_details['email']
        token = existing_user_details['token']
        number_of_posts = self._get_number_of_posts_for_current_user(user_index)
        created_post_id_list = list()
        for each_post in existing_user_details['posts'][:number_of_posts]:
            post_info = self._make_a_user_create_single_post(token=token, post=each_post)
            created_post_id_list.append(post_info['id'])
        self._set_post_ids_list_for_signed_up_user(user_index, created_post_id_list)
        print("User ( email: {} ) has created {} posts".format(email, number_of_posts))

    def _make_a_user_create_single_post(self, token, post):
        url_segments = [BASE_URL, self.url_endpoints['create_new_post']]
        header = self._get_valid_header_with_token(token=token)
        return self._make_post_request(url_segs=url_segments, header=header, payload=post)

    # Following functions are for implementing the requirement given in the doc
    # Strategy :
    # 1. Get a dict => { user's index : number of posts with zero likes }
    # 2. Get a dict => { post's id : user's index }
    # 3. Get a list => [ unique post id's ] for user to like

    # To select post at random, we need the list of post's available for user to like (#3)
    # I'll use the function _get_list_of_posts_user_can_like to build this list, where
    # I'll discard all the posts from current user and for rest of them we'll check in (#1) if user has no posts
    # with 0 likes we'll discard it's posts as well.

    def _get_user_index_to_num_of_posts_with_no_likes_mapping(self):
        # at first no post will have likes
        return self.user_index_to_number_of_posts_mapping

    def _get_post_id_to_user_index_mapping(self):
        return {each_post_id:each_user_index
                for each_user_index in self.user_index_to_created_post_id_list_mapping.keys()
                for each_post_id in self.user_index_to_created_post_id_list_mapping[each_user_index]}

    """
    Decrease the count of post with no likes for a creator(user).
    If the post is being liked for the first time.
    """
    def _decrease_the_count_of_post_with_no_likes_for_a_user(self, post_id):
        # get the user index who created this post
        if post_id in self.post_id_to_user_index_mapping.keys():
            post_creator_index = self.post_id_to_user_index_mapping[post_id]
            # following check is unnecessary, still keep it. It makes the implication explicit
            if self.user_index_to_num_of_posts_with_no_likes_mapping[post_creator_index] > 0:
                self.user_index_to_num_of_posts_with_no_likes_mapping[post_creator_index] -= 1
            return True
        return False

    def _remove_a_post_id_to_user_index_mapping(self, post_id):
        if post_id in self.post_id_to_user_index_mapping.keys():
            del self.post_id_to_user_index_mapping[post_id]
            return True
        return False

    def _get_list_of_posts_user_can_like(self, user_index):
        post_ids_user_can_like = list()

        for temp_user_index in self.user_index_to_created_post_id_list_mapping.keys():
            # user can't like their own post
            # user can't like post of other user if he/she do not have any post with zero like
            if temp_user_index != user_index and self.user_index_to_num_of_posts_with_no_likes_mapping[temp_user_index] > 0:
                post_ids_user_can_like.extend(self.user_index_to_created_post_id_list_mapping[temp_user_index])
        return post_ids_user_can_like

    def make_users_like_post_of_other_users(self):
        # Get the users in order of number of posts they have created
        # Note: Next user who likes the post is the one with most number of posts
        list_of_users_ordered_by_number_of_post = sorted(self.user_index_to_number_of_posts_mapping.items(),
                                                         key=lambda item: item[1],
                                                         reverse=True)

        self.user_index_to_num_of_posts_with_no_likes_mapping = self._get_user_index_to_num_of_posts_with_no_likes_mapping()
        # we are going to store this only till a post gets its first like.
        # this provides us the facility to keep track of posts with no like
        self.post_id_to_user_index_mapping = self._get_post_id_to_user_index_mapping()

        for (user_index, number_of_posts) in list_of_users_ordered_by_number_of_post:
            # the like op will only continue if there is at least one post with no likes
            if len(self.post_id_to_user_index_mapping) > 0:
                post_ids_a_user_can_like = self._get_list_of_posts_user_can_like(user_index)
                self._make_a_user_like_multiple_posts(user_index, post_ids_a_user_can_like)
            else:
                print("Terminating the like operation. There are no more posts with zero likes !")
                break
        return

    def _make_a_user_like_multiple_posts(self, user_index, post_ids_user_can_like):
        # Randomly choose indices of post id user is going to like
        num_of_legal_likes = self.max_likes_per_user \
            if self.max_likes_per_user <= len(post_ids_user_can_like)\
            else len(post_ids_user_can_like)
        post_id_index_to_be_liked_by_user = random.sample(range(len(post_ids_user_can_like)),
                                                          num_of_legal_likes)
        auth_token = self.signed_up_users[user_index]['token']
        for each_index in post_id_index_to_be_liked_by_user:
            self._make_a_user_like_single_post(auth_token, post_ids_user_can_like[each_index])

    def _get_if_user_likes(self):
        rand = random.randint(0, 1)
        return True if rand == 1 else False

    # Implementing a variation where, user can dislike the post as well
    def _make_a_user_like_single_post(self, token, post_id):
        if self._get_if_user_likes():
            url_segments = [BASE_URL, self.url_endpoints['like_a_post'], post_id]
        else:
            url_segments = [BASE_URL, self.url_endpoints['dislike_a_post'], post_id]
        header = self._get_valid_header_with_token(token=token)
        # I'll assume that this request will pass successfully
        self._decrease_the_count_of_post_with_no_likes_for_a_user(post_id)
        # Delete the entry for post id in postid to user index mapping
        self._remove_a_post_id_to_user_index_mapping(post_id)
        return self._make_patch_request(url_segs=url_segments, header=header)

    def request_get(self, secondary_url, id=None):
        user_token = self.signed_up_users[0]['token']
        header = self._get_valid_header_with_token(token=user_token)
        url_segments = [BASE_URL, secondary_url]
        if id is not None:
            url_segments.append(id)
        return self._make_get_request(url_segs=url_segments, header=header)

    def get_all_posts(self):
        return self.request_get(self.url_endpoints['get_all_posts'])

    def get_all_users(self):
        return self.request_get(self.url_endpoints['get_all_users'])

    def get_all_posts_in_detail(self):
        all_detailed_posts = list()
        for each_user in self.signed_up_users:
            for each_post_id in each_user['post_ids_list']:
                all_detailed_posts.append(
                    self.request_get(self.url_endpoints['get_post_details'], id=each_post_id)
                )
        return all_detailed_posts

    def get_all_users_in_detail(self):
        all_detailed_users = list()
        for each_user in self.signed_up_users:
            all_detailed_users.append(
                self.request_get(self.url_endpoints['get_user_details'], id=each_user['id'])
            )
        return all_detailed_users
