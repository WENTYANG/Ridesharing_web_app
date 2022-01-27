from django.urls import path
from .views import(
    RideListView,
    RideDetailView,
    RideCreateView,
    RideUpdateView,
    RideDeleteView,
)
from . import views

urlpatterns = [
    path('', RideListView.as_view(), name='rides-home'), #default look for <app>/<model>_<viewtype>.html (ride/ride_list.html)
    path('rides/<int:pk>/', RideDetailView.as_view(), name='ride-detail'),    #<int:pk> set variables in the path, the variable pk will be passed to the view
    path('rides/<int:pk>/update/', RideUpdateView.as_view(), name='rides-update'),
    path('rides/<int:pk>/delete/', RideDeleteView.as_view(), name='rides-delete'),
    path('rides/new/', RideCreateView.as_view(), name='ride-create'),         
    path('about/', views.about, name='rides-about'),
]