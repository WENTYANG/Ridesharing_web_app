from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import DriverInfo, Profile ,DriverInfo
from django.core.exceptions import ObjectDoesNotExist

@receiver(post_save, sender=User)   #When a user is saved, send a signal to the receiver -- create_profile function
def create_profile(sender, instance, created, **kwargs):    #If the user is created, then create a Profile object with the user = the instance of the user that is created
    if created:
        Profile.objects.create(user=instance)   #Profile是models里的class

@receiver(post_save, sender=User)   #When a user is saved, save the profile
def save_profile(sender, instance, created, **kwargs):
    instance.profile.save()         #profile是views里的function

@receiver(post_save, sender=User)   #When a user is saved, send a signal to the receiver -- create_profile function
def create_driver(sender, instance, created, **kwargs):    #If the user is created, then create a Profile object with the user = the instance of the user that is created
    # if created:
    #     DriverInfo.objects.create(user=instance)   #DriverInfo是models里的class
    try:
        instance.driverinfo.save()
    except ObjectDoesNotExist:
        DriverInfo.objects.create(user=instance)

# @receiver(post_save, sender=User)   #When a user is saved, save the profile
# def save_driver(sender, instance, created, **kwargs):
#     instance.driverinfo.save()         #driverinfo是views里的function