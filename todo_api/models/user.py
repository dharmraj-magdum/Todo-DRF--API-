from typing import Any
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

#  Custom User Manager inherited from djangos baseuserManager
# this is responsible for creating users (especialy with cli or admin pannel)


class UserManager(BaseUserManager):
    def create_user(self, name, email, password=None):
        """
        Creates and saves a User with the given email, name and password.
        """
        # print("Creates and saves a User with the given email, name and password.")
        # print(name, email, password)
      #   //if email is not provided then we cannot create user
        if not email:
            raise ValueError('User must have an email address')

      # //create user with given values
        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )
        # set password to user sepeartedly to put hashed one in DB
        # print("---------password", password)
        user.set_password(password)
        # save the user in DB
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None):
        """
        Creates and saves a superuser with the given email, name and password.
        """
        # print(name, email, password)
        # very much similar to normal user with added authorization
        user = self.create_user(
            name,
            email,
            password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


# CustomUser Model which have defaultdjango feactures with our added feat
class User(AbstractBaseUser):
    # define fields as we normaly do in  model
    email = models.EmailField(
        verbose_name='Email',
        max_length=200,
        unique=True,
    )
    # for email we consider it as unique identifire
    # verbose_name is name for cli/admin pannel user creation field name
    name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # IMP we have specifiy manager
    objects = UserManager()

    # Mark the email as a username for login credentials
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name',]

    def __str__(self):
        return self.email

    # ---------------------------------------------------------------------
    # below funtions are to set permissions we give only to admin
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
