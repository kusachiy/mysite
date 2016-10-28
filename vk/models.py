from django.db import models
from django.contrib.auth.models import User


class Person(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=30, unique=True)
    password = models.CharField(max_length=30)
    birthday = models.DateField()
    avatar = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Post(models.Model):
    id = models.AutoField(primary_key=True)
    wall_id = models.IntegerField()
    body = models.TextField()
    author = models.ForeignKey(Person)
    timestamp = models.DateTimeField(auto_now_add=True)


class Friends(models.Model):
    id = models.AutoField(primary_key=True)
    user1 = models.ForeignKey(Person)
    user2 = models.ForeignKey(Person)
    relationship = models.IntegerField()
