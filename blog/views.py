from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import(
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    )
from .models import Post

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
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context) #pass information into templates, open home.html
#template can access the keys in the dictionary posts

#class based view -- list view, to list all the posts
class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html' #convention: <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']

#class based view -- detail view, to display the information of a specific post
class PostDetailView(DetailView):
    model = Post
    
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user    #Set the author before submitting the form
        return super().form_valid(form)             #Run the form_valid in the parent class

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user    #Set the author before submitting the form
        return super().form_valid(form)             #Run the form_valid in the parent class

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def about(request):
    return render(request, 'blog/about.html', {'title': 'About'}) #title is displayed on the browser tab
