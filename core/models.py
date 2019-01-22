from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class UserAdvInfo(models.Model):
    user_twitter_handle = models.CharField(max_length=255, blank=True, null=True)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    company_location = models.TextField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.user_twitter_handle


class UserManager(BaseUserManager):

    def create_user(self, username, email, password=None, adv_info=''):
        """Creates and saves a new user"""
        if not username:
            raise ValueError("Username is mandatory")
        if not email:
            raise ValueError("Email is mandatory")
        user = self.model(username=username, email=self.normalize_email(email), adv_info=adv_info)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, email, password):
        """Create user with superuser abilities"""
        if not password:
            raise ValueError("Superuser needs to have password")
        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)       # user needs to be saved if one has changed it's param
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model that supports using email instead of username
    """
    username = models.CharField(max_length=255, unique=True, db_index=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    adv_info = models.OneToOneField(UserAdvInfo, blank=True, related_name="post_like", on_delete=models.PROTECT)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email


class Post(models.Model):
    """
    Create posts - will have many to one relationship with any user
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=60, blank=False, unique=True, db_index=True)
    fake_tweet = models.TextField(max_length=1000, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, db_index=True)
    liked_by = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="post_liked_by")
    disliked_by = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="post_disliked_by")

    def __str__(self):
        return self.title
