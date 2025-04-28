import random
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.models import User
from django.core.validators import RegexValidator, EmailValidator 
from django.conf import settings
from django.utils import timezone
from datetime import timedelta


# Create your models here.

phone_validator = RegexValidator(
    regex=r'^\d{11}$',
    message="Phone number must be exactly 11 digits."
)
class UserManager(BaseUserManager):
    def create_user(self,phone,email,username,password=None):
        if not phone:
            raise ValueError("Phone number is required.")
        user = self.model(phone=phone,email=email,username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password):
        user = self.create_user(phone, password)
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser):
    phone  = models.CharField(max_length=11,validators=[phone_validator])
    email = models.EmailField(unique=True,max_length=155)
    username = models.CharField(max_length=100,unique=True)
    is_staff = models.BooleanField(default=False)
    is_active =models.BooleanField(default=False)
    user_registere_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

    objects = UserManager()

    USERNAME_FIELD =  "email"
    


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=166)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.full_name


class OTP(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    count_attempt = models.IntegerField(default=0)



    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=10)

    def generate_otp(self):
        self.code = str(random.randint(10000,999999))
        self.created_at = timezone.now()
        self.is_verfied = False
        self.count_attempt = 0
        self.save() 

    def verifing_otp(self,code):
        if not is_expired():
            if self.code == code:
                return True
        else:
            return "OTP is Expired!"

