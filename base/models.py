from operator import mod
from statistics import mode
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.


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

    def __str__(self):
        return str(self.user)


class Blog(models.Model):
    id = models.AutoField
    title = models.CharField(max_length=50)
    body = models.TextField()
    likes = models.PositiveBigIntegerField(default=0)
    liked = models.ManyToManyField(Profile, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now=True)
    publish = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
