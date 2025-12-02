from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView, PostDeleteView, PostUpdateView, PostDraftListView, PostArchiveListView

urlpatterns = [
    path("list/", PostListView.as_view(), name="post_list"),
    path("draftlist/", PostDraftListView.as_view(), name="draft_list"),
    path("archivelist/", PostArchiveListView.as_view(), name="archive_list"),
    path("", PostListView.as_view(), name="post_list"),
    path("detail/<int:pk>/", PostDetailView.as_view(), name="post_detail"),
    path("new/", PostCreateView.as_view(), name="post_new"),
    path("update/<int:pk>/", PostUpdateView.as_view(), name="post_update"),
    path("delete/<int:pk>/", PostDeleteView.as_view(), name="post_delete")
]