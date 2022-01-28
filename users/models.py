from django.db import models
from django.contrib.auth.models import User
from PIL import Image
# Create your models here.

#Choices: first is the actual value set in the module, second is human-readable text
VEHICLE_TYPE_CHOICES = [
    ("SEDAN", "SEDAN"),
    ("COMPACT", "COMPACT"),
    ("SUV", "SUV"),
    ("MINIVAN", "MINIVAN"),
    ("TRUCK", "TRUCK"),
    ("COUPE", "COUPE"),
    ("OTHER", "OTHER")
]

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) #CASCADE: If the user is deleted, then the profile is deleted as well
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs) #run the parent's save method

        img = Image.open(self.image.path)

        #overwrite the larger image to a limited sizes
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

class DriverInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='driverinfo') #CASCADE: If the user is deleted, then the profile is deleted as well
    licence = models.CharField(max_length=10, default='')
    max_passengers = models.PositiveIntegerField(default = 0)
    vehicle_type = models.CharField(max_length=10, choices=VEHICLE_TYPE_CHOICES, default="SEDAN")
    special_info = models.TextField(blank = True, default = '') #blank = True: required=False, meaning it's optional field

    def __str__(self):
        return f'{self.user.username} DriverInfo'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs) #run the parent's save method
