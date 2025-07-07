from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Custome user model extending Django AbstractUser
    # Adds additional fields: email(unique,Bio, add avater image)
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    # Use username as the unique identifier for authentication
    USERNAME_FIELD = "username"
    # Ensure email is also collected during createsuperuser or user creation
    REQUIRED_FIELDS = ["email"]


class Category(models.Model):
    # Category for organizing blog posts.
    # Each category has a name and optional description. Posts can belong to multiple categories.
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    categories = models.ManyToManyField(
        Category,
        related_name="posts",
        # Allow posts without any category
        blank=True, 
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Show newest posts first by default
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("post_detail", args=[self.pk])


class Comment(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    author_name = models.CharField(max_length=80, blank=True)  # for anonymous
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ["created_at"]