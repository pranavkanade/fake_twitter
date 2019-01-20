# Prak-Net:

Building a simple twitter

- Create new user
```bash
curl -X POST -d "email=user1@mail.com&username=user1&password=user1pass" http://localhost:8000/api/user/signup/
```

- Get JWT auth token
```bash
curl -X POST -H "Content-Type: application/json" -d '{"username":"admin","password":"password123"}' http://localhost:8000/api/user/login/
```

Feature API endpoints List -
1. Create Users (signup)                        : `/api/user/signup/` (POST)
1. Login (SessionAuthentication not done)       : `/api/user/login/` (Returns the JWT token) (POST)
1. Get JWT token                                : `/api/user/login/` (POST)
1. Renew JWT token                              : `/api/user/token/refresh/` (POST)
1. Post - Create new post                       : `/api/post/` (POST)
1. Post - Show all the posts from all the users : `/api/post/` (GET)
1. Post - Show a post in detail                 : `/api/post/<id>/` (GET)
1. Post - Like a post                           : `/api/post/<id>/like/` (PATCH)
1. Post - Dislike a post                        : `/api/post/<id>/dislike/` (PATCH)
1. Post - Show posts made by current user       : `/api/post/me/` (GET)

> Above features are complete: IST, SUN Jan 20 - 4:17 PM 