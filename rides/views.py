from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import(
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    )
from .models import Ride
from django.contrib.auth.decorators import login_required
# from .forms import RideUpdateForm
from django.contrib import messages
from django.db.models import Q

#from django.http import HttpResponse
# posts = [       #list of dictionaries, each dict is a post
#     {
#         'author': 'A',
#         'title': 'Blog Post 1',
#         'content': 'First post',
#         'date_posted': 'August 27, 2022'
#     },
#     {
#         'author': 'B',
#         'title': 'Blog Post 2',
#         'content': 'Second post',
#         'date_posted': 'August 28, 2022'
#     }
# ]


def home(request):
    context = {         
        'rides': Ride.objects.all()
    }
    return render(request, 'rides/home.html', context) #pass information into templates, open home.html
#template can access the keys in the dictionary posts

#class based view -- list view, to list all the posts
class RideListView(ListView):
    model = Ride
    template_name = 'rides/home.html' #convention: <app>/<model>_<viewtype>.html
    context_object_name = 'rides'
    ordering = ['-date_posted']

#class based view -- detail view, to display the information of a specific post
class RideDetailView(DetailView):
    model = Ride
    
class RideCreateView(LoginRequiredMixin, CreateView):
    model = Ride
    fields = ['destination', 'arrival_time', 'num_passengers', 'vehicle_type', 'can_be_shared', 'special_requests']

    def form_valid(self, form):
        form.instance.owner = self.request.user    #Set the author before submitting the form
        form.instance.driver = self.request.user
        return super().form_valid(form)             #Run the form_valid in the parent class

class RideUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Ride
    fields = ['destination', 'arrival_time', 'num_passengers', 'vehicle_type', 'can_be_shared', 'special_requests']

    def form_valid(self, form):
        form.instance.owner = self.request.user    #Set the author before submitting the form
        return super().form_valid(form)             #Run the form_valid in the parent class

    def test_func(self):
        ride = self.get_object()
        if (self.request.user == ride.owner) and (ride.owner ==  ride.driver):         
            #owner is the same as driver, meaning the ride is still open. Owner can edit the ride as long as it's not confirmed
            return True
        return False

class RideDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Ride
    success_url = '/'       #Need the '/' to resolve to the home address

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.owner:
            return True
        return False

#The owned or shared ride of one user
@login_required
def my_joined_ride(request):
    context = {         
        'owner_rides': request.user.ride_onwer.all(),
        'sharer_rides': request.user.ride_sharer.all()
    }
    return render(request, 'rides/my_joined_ride.html', context)

def my_driven_ride(request):
    context = {         
        'driver_rides': request.user.ride_driver.filter(~Q(driver=request.user))
    }
    return render(request, 'rides/my_driven_ride.html', context)

def myrides(request):
    return render(request, 'rides/myrides.html', {'title': 'About'}) #title is displayed on the browser tab
