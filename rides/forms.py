from django import forms
from .models import Ride

class SharerSearchForm(forms.Form):
    destination = forms.CharField(max_length=100)
    early_time = forms.DateTimeField()
    late_time = forms.DateTimeField()
    num_passengers = forms.IntegerField()

# class RideCreationForm(forms.ModelForm):
#     class Meta:
#         model = Ride
#         fields = ['destination', 'arrival_time', 'num_passengers', 'vehicle_type', 'shared', 'special_requests']

# class RideUpdateForm(forms.ModelForm):
#     # arrival_time = forms.DateTimeField(attrs={'type':'datetime-local'})
#     class Meta:
#         model = Ride
#         fields = ['destination', 'arrival_time', 'num_passengers', 'vehicle_type', 'shared', 'special_requests', 'complete', 'driver', 'date_posted', 'owner']

    # destination = models.CharField(max_length=100)
    # arrival_time = models.DateTimeField()
    # num_passengers = models.PositiveIntegerField(default=1)
    # vehicle_type = models.CharField(blank=True, max_length=10, choices=VEHICLE_TYPE_CHOICES)
    # shared = models.BooleanField()
    # special_requests = models.TextField(blank=True)
    # complete = models.BooleanField()
    # driver = models.CharField(max_length=100)
    # date_posted = models.DateTimeField(default=timezone.now)
    # owner = models.ForeignKey(User, on_delete=models.CASCADE)   #If the user is deleted, the post is deleted as well