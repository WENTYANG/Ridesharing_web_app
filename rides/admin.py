from django.contrib import admin
from .models import Membership, Ride

# Register your models here.
admin.site.register(Ride)
admin.site.register(Membership)