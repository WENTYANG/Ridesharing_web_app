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
from .forms import SharerSearchForm
from django.utils import timezone

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
    # pass information into templates, open home.html
    return render(request, 'rides/home.html', context)
# template can access the keys in the dictionary posts

# class based view -- list view, to list all the posts


class RideListView(ListView):
    model = Ride
    template_name = 'rides/home.html'  # convention: <app>/<model>_<viewtype>.html
    context_object_name = 'rides'
    ordering = ['-date_posted']

# class based view -- detail view, to display the information of a specific post


class RideDetailView(DetailView):
    model = Ride


class RideCreateView(LoginRequiredMixin, CreateView):
    model = Ride
    fields = ['destination', 'arrival_time', 'num_passengers',
              'vehicle_type', 'can_be_shared', 'special_requests']

    def form_valid(self, form):
        # Set the author before submitting the form
        form.instance.owner = self.request.user
        form.instance.driver = self.request.user
        form.instance.num_all = form.instance.num_passengers
        return super().form_valid(form)  # Run the form_valid in the parent class


class RideUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Ride
    fields = ['destination', 'arrival_time', 'num_passengers',
              'vehicle_type', 'can_be_shared', 'special_requests']

    def form_valid(self, form):
        # Set the author before submitting the form
        form.instance.owner = self.request.user
        return super().form_valid(form)  # Run the form_valid in the parent class

    def test_func(self):
        ride = self.get_object()
        if (self.request.user == ride.owner) and (ride.owner == ride.driver)\
            and (ride.complete==False):
            # owner is the same as driver, meaning the ride is still open. Owner can edit the ride as long as it's not confirmed
            return True
        return False


class RideDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Ride
    success_url = '/'  # Need the '/' to resolve to the home address

    def test_func(self):
        ride = self.get_object()
        if self.request.user == ride.owner and ride.complete==False:
            return True
        return False

# The owned or shared ride of one user


@login_required
def my_joined_ride(request):
    context = {
        'owner_rides': request.user.ride_onwer.filter(complete=False),
        'sharer_rides': request.user.ride_sharer.filter(complete=False)
    }
    return render(request, 'rides/my_joined_ride.html', context)

@login_required
def my_driven_ride(request):
    context = {
        'driver_rides': request.user.ride_driver.filter(~Q(owner=request.user))
    }
    return render(request, 'rides/my_driven_ride.html', context)

@login_required
def myrides(request):
    # title is displayed on the browser tab
    return render(request, 'rides/myrides.html', {'title': 'About'})

@login_required
def search_ride_driver(request):
    if(request.user.driverinfo.licence != ''):  # The user has registered as a driver
        context = {
            'open_rides': Ride.objects.filter(
                ~Q(owner=request.user),
                Q(vehicle_type=request.user.driverinfo.vehicle_type)|Q(vehicle_type=''),
                is_open=True,
                num_all__lt=request.user.driverinfo.max_passengers,
                )
        }
        return render(request, 'rides/search_ride.html', context)
    else:
        # If not currently a driver, go to driver register page
        return render(request, 'rides/not_driver.html')

@login_required
def search_ride_sharer(request):
    if request.method == 'POST':  # When we submit our form and possibly update the data
        # SharerSearchForm is not a model form, so we don't have to pass an instance
        s_form = SharerSearchForm(request.POST)
        # Update the forms
        if s_form.is_valid():
            # s_form.save()
            context = {
                'open_rides': Ride.objects.filter(\
                    is_open=True,
                    arrival_time__gt=s_form.cleaned_data['early_time'],
                    arrival_time__lt=s_form.cleaned_data['late_time'],
                    destination=s_form.cleaned_data['destination'],
                )
            }
            return render(request, 'rides/search_ride.html', context)
    else:
        nowtime = timezone.now()
        s_form = SharerSearchForm(
            initial={
                'destination': '',
                'early_time': nowtime,
                'late_time': nowtime,
                'num_passengers': 1,
            }
        )
    # pass in for template
    return render(request, 'rides/search_ride_sharer.html', {'form': s_form})

@login_required
def claim_service(request, pk):
    print(pk)
    #Check if user is a valid driver
    driver = request.user
    if(driver.driverinfo.licence != ''):
        #Check if the order status matches the driver's information
        order = Ride.objects.get(pk=pk)
        if(order.is_open==True)\
            and (order.vehicle_type==driver.driverinfo.vehicle_type or order.vehicle_type=='')\
            and (order.num_all<=driver.driverinfo.max_passengers):
            # or order.vehicle_type==None
            order.driver=driver
            order.is_open=False
            print(order.driver.driverinfo.vehicle_type)
            order.save()
            messages.success(request, f'The order has been accepted!')
        elif(order.is_open==False):
            #If the order has already been taken
            messages.warning(request, f'The order has already been taken!')
        else:
            #If the status doesn't match
            messages.warning(request, f'The order does not match your driver information!')
        return redirect('ride-detail', pk=pk)
    else:
        # If not currently a driver, go to driver register page
        return render(request, 'rides/not_driver.html')

@login_required
def order_complete(request, pk):
    driver = request.user
    order = Ride.objects.get(pk=pk)
    if(driver.driverinfo.licence != '' and order.driver==driver and order.owner!=driver):
        if(order.complete==True):
            messages.warning(request, f'The order is already completed!')
        else:
            order.complete=True
            order.save()
            messages.success(request, f'The order has been completed!')
    return redirect('ride-detail', pk=pk)
        #return render(request, 'rides/order_complete.html')