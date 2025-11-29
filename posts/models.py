from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model

# Create your models here.
class Status(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.CharField(max_length=256, help_text="Write a description about status")

    class Meta:
        verbose_name_plural = "Status"
        
    def __str__(self):
        return self.name
    
class Post(models.Model):
    title = models.CharField(max_length=128)
    subtitle = models.CharField(max_length=256, blank=True)
    body = models.TextField()
    image = models.ImageField(upload_to='images/', blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='posts'
    )

    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        null=False,
        related_name='posts'
    )

    def __str__(self):
        return f"{self.title} by {self.author}"

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"pk": self.pk})

class Comment(models.Model):
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='comments'
    )

    def __str__(self):
        return f"Comment by {self.author} on {self.post}"