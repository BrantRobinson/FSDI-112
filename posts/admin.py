from django.contrib import admin

# Register your models here.
from .models import Post, Comment, Status

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Status)