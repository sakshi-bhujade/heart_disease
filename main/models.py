from django.contrib.auth.models import User
from django.db import models

# Create your models here.

gender = (("m", "MALE"), ("f", "FEMALE"), ("o", "OTHER"))


class Profile(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)

    email = models.CharField(max_length=150)
    dob = models.DateField()

    # sex=models.CharField(choices=gender,max_length=128)
    def __str__(self):
        return self.email
