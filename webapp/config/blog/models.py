from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.CharField(max_length=255)
    featured = models.BooleanField(default=True)
    published = models.BooleanField(default=True)

    # SEO fields
    meta_title = models.CharField(
        max_length=60,
        blank=True,
        help_text="Max 60 characters for SEO"
    )
    meta_description = models.CharField(
        max_length=160,
        blank=True,
        help_text="Max 160 characters for SEO"
    )

    meta_keywords = models.CharField(
        max_length=255,
        blank=True,
        help_text="Comma-separated keywords"
    )
    canonical_url = models.URLField(
        blank=True,
        help_text="Leave empty to use default post URL"
    )

    # Open Graph fields
    og_title = models.CharField(max_length=60, blank=True)
    og_description = models.CharField(max_length=160, blank=True)
    # og_image = models.ImageField(
    #     upload_to='og_images/',
    #     blank=True,
    #     null=True
    # )
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'D', 'DRAFT'
        PUBLISHED = 'P', 'PUBLISHED'
        UNPUBLISHED = 'U', 'UNPUBLISHED'

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    content = models.TextField()
    featured = models.BooleanField(default=True)
    status = models.CharField(max_length=1, choices=Status.choices, default=Status.PUBLISHED)
    category = models.ForeignKey(Category, related_name='posts', on_delete=models.PROTECT)
    author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)

    # SEO fields
    meta_title = models.CharField(
        max_length=60,
        blank=True,
        help_text="Max 60 characters"
    )
    meta_description = models.CharField(
        max_length=160,
        blank=True,
        help_text="Max 160 characters"
    )
    meta_keywords = models.CharField(
        max_length=255,
        blank=True,
        help_text="Comma-separated keywords"
    )
    canonical_url = models.URLField(
        blank=True,
        help_text="Leave empty to use default post URL"
    )

    # Open Graph
    og_title = models.CharField(max_length=60, blank=True)
    og_description = models.CharField(max_length=160, blank=True)
    # og_image = models.ImageField(
    #     upload_to='og_images/',
    #     blank=True,
    #     null=True
    # )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    name = models.CharField(max_length=100)
    text = models.TextField()
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.name} on {self.post.title}'
    
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f'{self.name} ({self.message})'
    

