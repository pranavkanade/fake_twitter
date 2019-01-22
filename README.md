# fake twitter:

Building a simple fake twitter rest api

## General Info:

1. `prak_net` - Django main project directory
1. `core` - This is the core module which used for putting models together.
1. `user` - This app provides all the user related APIs
1. `post` - This app provides all the post related APIs

## Before You RUN:
1. **Please add API keys for Hunter and Clearbit** - `fake_twitter/prak_net/settings.py`
2. Create new python3.7 environment and install all dependencies from `requirements.txt`

## Verifying the APIs -

### Steps to verify

1. I've created a bot script that tests the working of all APIs - `test_bot.py`. You can use this to interact with it.
2. Run server in terminal 1 - `rm -rf db.sqlite3 && python manage.py makemigrations && python manage.py migrate && python manage.py runserver`
3. In terminal 2, run - `test_bot.py`

### Input data -

1. Bot uploads all the data from `fake_twitter/bot/data/fake_twitter_test_data.json`. And then performs operations mentioned in the assignment.
1. The `fake_twitter_test_data.json` contains dummy data for 9 different users.
1. You may want to add more data according to your need.

### Result - `fake_twitter/bot/data/results/`
* There will be four files at the end -

1. `all_users.json`: This file contains output of `/api/user/all/` API. Which is not the complete information. For advance info collected from Clearbit, check file - 2.
2. `all_detailed_users.json`: This file contains all the info we have collected on a user. This is file is created by querying - `/api/user/<id>/` API endpoint.
3. `all_posts.json`: This file has minimum info regarding the posts created. Endpoint used - `/api/post/`
4. `all_detailed_posts.json`: It contains all their is to a post. With all info on users that may have liked or disliked the post. Endpoint used - `/api/post/<id>/`


### Change Bot Config -

1. The config that bot uses to operate can be found at - `fake_twitter/bot/config`.
2. As there is limited data please consider following guidelines for assigning the values in `fake_twitter/bot/config/bot_config.json`.
```
  number_of_users <= 9,
  max_posts_per_user <= 10,
  max_likes_per_user <= 50 
```
3. The extreme cases are not tested, due to limitations on Clearbit's API usage. So, things might start breaking! :D


## Feature API endpoints List -

1. Create Users (signup)                        : `/api/user/signup/` (POST)
1. Login                                        : `/api/user/login/` (Returns the JWT token) (POST)
1. Get JWT token                                : `/api/user/login/` (POST)
1. Renew JWT token                              : `/api/user/token/refresh/` (POST)
1. Get Users list                               : `/api/user/all/` (GET)
1. Get Details of a User                        : `/api/user/<id>/` (GET)
1. Get Details of logged in user                : `/api/user/me/` (GET)
1. Create new post                              : `/api/post/` (POST)
1. Show all the posts from all the users        : `/api/post/` (GET)
1. Show a post in detail                        : `/api/post/<id>/` (GET)
1. Like a post                                  : `/api/post/<id>/like/` (PATCH)
1. Dislike a post                               : `/api/post/<id>/dislike/` (PATCH)
1. Show posts made by current user              : `/api/post/me/` (GET)


* List of user emails -
```text
anand@persistent.com
alex@clearbit.com
monaweng@google.com
miguelf@google.com
afried@google.com
kwalstra@google.com
bernardo.zamora@microsoft.com
sunil.kamath@microsoft.com
dmcmahon@microsoft.com
harrycal@microsoft.com
dana.scully@fbi.gov
lisa.fischer@cnn.com
sara.obrien@cnn.com
jeremy.herb@cnn.com
christopher.carbone@foxnews.com
suzanne.scott@foxnews.com
brian.wilson@foxnews.com
ashish.shetty@tcs.com
```


#### IMP links -
* [Clearbit API python implementation](https://github.com/clearbit/clearbit-python)
