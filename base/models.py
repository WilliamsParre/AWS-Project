from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.


# class Blog(models.Model):
#     id = models.AutoField
#     title = models.CharField(max_length=50)
#     body = models.TextField()

class Profile(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10, choices=[(
        'Male', 'Male'), ('Female', 'Female'), ('Others', 'Others')])
    profile_pic = models.ImageField(
        default="default_profile_pic.jpg")
    phone_no = models.BigIntegerField(validators=[
        MaxValueValidator(9999999999),
        MinValueValidator(1111111111)
    ], blank=False)
