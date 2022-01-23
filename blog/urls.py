from django.urls import path
from .views import(
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
)
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'), #default look for <app>/<model>_<viewtype>.html (blog/post_list.html)
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),    #<int:pk> set variables in the path, the variable pk will be passed to the view
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),         
    path('about/', views.about, name='blog-about'),
]