# Prak-Net:

Building a simple twitter

- Create new user
```bash
curl -X POST -d "email=user1@mail.com&username=user1&password=user1pass" http://localhost:8000/user/create/
```

- Get JWT auth token
```bash
curl -X POST -H "Content-Type: application/json" -d '{"username":"admin","password":"password123"}' http://localhost:8000/api-token-auth/
```
