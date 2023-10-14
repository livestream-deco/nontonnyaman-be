from django.db import models
import datetime
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from stadium.models import Stadium

class MyAccountManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        extra_fields.setdefault('is_staff', False)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        return self.create_user(email, password, **extra_fields)

class Account(AbstractBaseUser):
    email = models.CharField(max_length=20, primary_key=True, blank=True)
    name = models.CharField(max_length=40, blank=True)
    date = models.DateField(("Date"), default=datetime.date.today)
    is_staff = models.BooleanField(default=False)  # Identifies staff members
    has_chose = models.BooleanField(default=False)  # Identifies if the user has chosen a staff
    stadium = models.ForeignKey(Stadium, related_name='staff', on_delete=models.SET_NULL, null=True, blank=True)
    staff_assistant = models.OneToOneField('StaffAssistant', on_delete=models.SET_NULL, null=True, blank=True)

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
    phone_number = models.CharField(max_length=10, blank=False)
    stadium = models.ForeignKey(Stadium, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.email

class StaffAssistant(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    staff = models.ForeignKey(StaffProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email
