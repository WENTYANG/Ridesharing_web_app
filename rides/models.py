from inspect import Attribute
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# class Post(models.Model):
#     title = models.CharField(max_length=100)
#     content = models.TextField()
#     date_posted = models.DateTimeField(default=timezone.now)
#     author = models.ForeignKey(User, on_delete=models.CASCADE)   #If the user is deleted, the post is deleted as well

#     def __str__(self):
#         return self.title

#     def get_absolute_url(self):
#         return reverse('post-detail', kwargs={'pk': self.pk})   #reverse will return the full url path as a string, 
#                                                                 #here we want to go to the detail page of thr post,
#                                                                 #using its primary key

VEHICLE_TYPE_CHOICES = [
    ("SEDAN", "SEDAN"),
    ("COMPACT", "COMPACT"),
    ("SUV", "SUV"),
    ("MINIVAN", "MINIVAN"),
    ("TRUCK", "TRUCK"),
    ("COUPE", "COUPE"),
    ("OTHER", "OTHER")
]

class Ride(models.Model):
    owner = models.ForeignKey(User, related_name='ride_onwer', on_delete=models.CASCADE)   #One to many, a ride has only one owner, while a user can own multiple rides
    
    #user includes owner, driver and user    
    destination = models.CharField(max_length=100)
    arrival_time = models.DateTimeField(help_text='Format: 2020-01-01 12:00')
    num_passengers = models.PositiveIntegerField(default=1)

    driver = models.ForeignKey(User, related_name='ride_driver', on_delete=models.DO_NOTHING, null=True, blank=True, default=None)
    sharer = models.ManyToManyField(User, related_name='ride_sharer', blank=True)

    vehicle_type = models.CharField(max_length=10, choices=VEHICLE_TYPE_CHOICES, blank=True) #Owner may specify a vehicle type when requesting a ride
    can_be_shared = models.BooleanField()
    special_requests = models.TextField(blank=True)
    
    complete = models.BooleanField(default=False)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('ride-detail', kwargs={'pk': self.pk})   #reverse will return the full url path as a string, 
                                                                #here we want to go to the detail page of thr post,
                                                                #using its primary key