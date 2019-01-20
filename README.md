# Prak-Net:

Building a simple twitter rest api

#### Before You RUN:
**Please add API keys for Hunter and Clearbit**



Feature API endpoints List -
1. Create Users (signup)                        : `/api/user/signup/` (POST)
1. Login (SessionAuthentication not done)       : `/api/user/login/` (Returns the JWT token) (POST)
1. Get JWT token                                : `/api/user/login/` (POST)
1. Renew JWT token                              : `/api/user/token/refresh/` (POST)
1. Get Users list                               : `/api/user/all/` (GET)
1. Get Details of a User                        : `/api/user/<id>/` (POST)
1. Get Details of logged in user                : `/api/user/me/` (POST)
1. Post - Create new post                       : `/api/post/` (POST)
1. Post - Show all the posts from all the users : `/api/post/` (GET)
1. Post - Show a post in detail                 : `/api/post/<id>/` (GET)
1. Post - Like a post                           : `/api/post/<id>/like/` (PATCH)
1. Post - Dislike a post                        : `/api/post/<id>/dislike/` (PATCH)
1. Post - Show posts made by current user       : `/api/post/me/` (GET)

> Above features are complete: IST, SUN Jan 21 - 3:17 AM

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


## IMP links -
* [Clearbit API python implementation](https://github.com/clearbit/clearbit-python)