from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=255, null=False)
    tag = models.CharField(max_length=255, null=False)

    def __str__(self):
        return self.name


def get_user_dir(request, filename):
    return f'event/{filename}'


class Image(models.Model):
    image = models.ImageField(upload_to=get_user_dir, blank=True, null=True)
    is_unique = models.BooleanField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)


class Event(models.Model):
    name = models.CharField(max_length=255, null=False)
    description = models.TextField()
    date = models.DateTimeField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    location = models.CharField(max_length=255, null=False)
    duration = models.IntegerField(default=60*60)
    organiser = models.ForeignKey(User, on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()
    is_premium = models.BooleanField()
    image = models.ForeignKey(Image, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class EventMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    

class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    is_paid = models.BooleanField()
    date = models.DateTimeField()
