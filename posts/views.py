from .models import Post
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)



class PostListView(ListView): 
    """
    PostListView retrieves all objects from the posts table in the database
    """
    template_name = "posts/list.html"
    model = Post
    context_object_name = "posts"

class PostDetailView(DetailView): 
    """
    PostListView retrieves one object from the posts table in the database
    """
    template_name = "posts/detail.html"
    model = Post
    context_object_name = "single_post"

class PostCreateView(CreateView): 
    """
    Render a from with the specified fields to create a new post object 
    """
    template_name = "posts/new.html"
    model = Post
    fields = ["title", "subtitle", "body", "image"]

    def form_valid(self, form):
        print(User.objects.all())
        form.instance.author = User.objects.filter(is_superuser=True).first()
        return super().form_valid(form)

class PostUpdateView(UpdateView): 
    """
    Render a form that will allow the user to update certain fields of their post
    """
    template_name = "posts/update.html"
    context_object_name = "single_post"
    model = Post
    fields = ["title", "subtitle", "body", "image"]

class PostDeleteView(DeleteView):
    """
    View used to delete a post
    """
    template_name = "posts/delete.html"
    model = Post
    context_object_name = "single_post"
    success_url = reverse_lazy("post_list")
