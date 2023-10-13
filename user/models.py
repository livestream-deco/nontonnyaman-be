from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import datetime
from stadium.models import Stadium

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
    email = models.CharField(max_length=20, primary_key=True, blank=True)
    name = models.CharField(max_length=40, blank=True)
    date = models.DateField(("Date"), default=datetime.date.today)
    is_staff = models.BooleanField(default=False)  # Identifies staff members
    stadium = models.ForeignKey(Stadium, related_name='staff', on_delete=models.SET_NULL, null=True, blank=True)
    # Add other common user fields as needed

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = MyAccountManager()

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return True

class StaffProfile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    staff_id = models.CharField(max_length=10, unique=True)
    department = models.CharField(max_length=40)
    is_available = models.BooleanField(default=True)  # Attribute for availability

    def __str__(self):
        return self.user.email

class AssistanceRequest(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    staff = models.ForeignKey(StaffProfile, on_delete=models.SET_NULL, null=True, blank=True)
    request_message = models.TextField()
    # Add timestamp or other fields as needed

    def __str__(self):
        return f"Assistance request from {self.user.email}"
