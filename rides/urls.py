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
    path('rides/<int:pk>/claim-service/', views.claim_service, name='claim-service'),
    path('rides/<int:pk>/share-ride', views.share_ride, name='share-ride'),
    path('rides/<int:pk>/order-complete/', views.order_complete, name='order-complete'),
    path('rides/<int:pk>/delete/', RideDeleteView.as_view(), name='rides-delete'),
    path('rides/<int:pk>/quit-sharing/', views.quit_sharing, name='quit-sharing'),
    path('rides/new/', RideCreateView.as_view(), name='ride-create'),         
    path('myrides/', views.myrides, name='rides-myrides'),
    path('my_joined_ride/', views.my_joined_ride, name='my_joined_ride'),
    path('my_driven_ride/', views.my_driven_ride, name='my_driven_ride'),
    path('search_ride_driver/', views.search_ride_driver, name='search_ride_driver'),
    path('search_ride_sharer/', views.search_ride_sharer, name='search_ride_sharer'),
]