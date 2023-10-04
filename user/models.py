from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import datetime

class MyAccountManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Users must have a valid email")
        
        user = self.model(
            email=email,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password):
        user = self.create_user(
            email=email,
            password=password,
        )
        user.is_staff = True
        user.save(using=self._db)
        return user
class Account(AbstractBaseUser):
    email = models.CharField(max_length=20,primary_key=True, blank=True)
    name = models.CharField(max_length = 40, blank = True)
    date = models.DateField(("Date"), default=datetime.date.today)
    is_staff = models.BooleanField(default=False)
    role_users = models.BooleanField(default=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = MyAccountManager()

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return True