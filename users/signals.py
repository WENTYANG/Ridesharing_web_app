from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile #,Driverinfo

@receiver(post_save, sender=User)   #When a user is saved, send a signal to the receiver -- create_profile function
def create_profile(sender, instance, created, **kwargs):    #If the user is created, then create a Profile object with the user = the instance of the user that is created
    if created:
        Profile.objects.create(user=instance)   #Profile是models里的class

@receiver(post_save, sender=User)   #When a user is saved, save the profile
def save_profile(sender, instance, created, **kwargs):
    instance.profile.save()         #profile是views里的function