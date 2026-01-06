from .models import Post
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin
)
from django.views.generic.edit import FormMixin
from .forms import CommentForm
from django.urls import reverse_lazy, reverse
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
    
    def get_queryset(self):
        user = self.request.user

        published = Post.objects.filter(status__name="Published").order_by("created_on").reverse()

        if user.is_authenticated:
            own_posts = Post.objects.filter(author=user).order_by("created_on").reverse()
            return (published | own_posts).distinct()
        return published
    
class PostDraftListView(LoginRequiredMixin, ListView):
    template_name = "posts/draftlist.html"
    model = Post
    context_object_name = 'draft_posts'

    def get_queryset(self):
        user = self.request.user
        drafts = Post.objects.filter(status__name="Draft", author = user).order_by("created_on").reverse()
        return drafts

class PostArchiveListView(LoginRequiredMixin, ListView):
    template_name = "posts/archivelist.html"
    model = Post
    context_object_name = 'archive_posts'

    def get_queryset(self):
        user = self.request.user
        drafts = Post.objects.filter(status__name="Archived", author = user).order_by("created_on").reverse()
        return drafts

class PostDetailView(FormMixin, DetailView): 
    """
    PostListView retrieves one object from the posts table in the database
    """
    template_name = "posts/detail.html"
    model = Post
    context_object_name = "single_post"
    form_class = CommentForm

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk':self.object.id})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all().order_by('-created_on')

        if self.request.user.is_authenticated:
            context['form'] = self.get_form()
        else:
            context['form'] = None  # optional, but explicit

        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            comment.author = request.user
            comment.save()
            return super().form_valid(form)
        else:
            return super().form_invalid(form)
    
class PostCreateView(CreateView): 
    """
    Render a from with the specified fields to create a new post object 
    """
    template_name = "posts/new.html"
    model = Post
    fields = ["title", "subtitle", "body", "image", "status"]

    def form_valid(self, form):
        form.instance.author = self.request.user 
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView): 
    """
    Render a form that will allow the user to update certain fields of their post
    """
    template_name = "posts/update.html"
    context_object_name = "single_post"
    model = Post
    fields = ["title", "subtitle", "body", "image", "status"]

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False
        

class PostDeleteView(LoginRequiredMixin, DeleteView):
    """
    View used to delete a post
    """
    template_name = "posts/delete.html"
    model = Post
    context_object_name = "single_post"
    success_url = reverse_lazy("post_list")
