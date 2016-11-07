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
    
    def __cmp__(self, other):
        if self.timestamp < other.timestamp:
            return 1
        elif self.timestamp > other.timestamp:
            return -1
        return 0


class Friends(models.Model):
    RELATIONSHIPS = (
        ('1', 'Subscriber'),
        ('3', 'Friends'),
        ('2', 'Master'),
        ('0', 'Neutral'),
    )

    id = models.AutoField(primary_key=True)
    user1 = models.IntegerField()
    user2 = models.IntegerField()
    relationship = models.IntegerField(max_length=1, choices=RELATIONSHIPS)
