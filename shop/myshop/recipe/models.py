from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from taggit.managers import TaggableManager

from images.models import Image

# Managers
class PublishedManager(models.Manager):
    def get_queryset(self):
        return (
            super().get_queryset().filter(status=Post.Status.PUBLISHED)
        )

# recipe Post Model
class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    class Category(models.TextChoices):  # Add category choices
        APPETIZER = 'AP', 'Appetizer'
        MAIN_COURSE = 'MC', 'Main Course'
        DESSERT = 'DE', 'Dessert'
        SALAD = 'SA', 'Salad'
        DRINK = 'DR', 'Drink'
        
    title = models.CharField(max_length=250)
    slug = models.SlugField(
        max_length=250,
        unique_for_date='publish'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='recipe_posts'
    )
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=2,
        choices=Status,
        default=Status.DRAFT
    )
    category = models.CharField(  # Add category field
        max_length=2,
        choices=Category.choices,
        default=Category.MAIN_COURSE
    )
    ingredients = models.TextField(default='No ingredients specified')  # New field for ingredients
    instructions = models.TextField(default='No instructions specified')
    image = models.ForeignKey(Image, related_name='recipes', on_delete=models.SET_NULL, null=True, blank=True)
    objects = models.Manager()  # The default manager.
    published = PublishedManager()  # Our custom manager.
    tags = TaggableManager(related_name='recipe_posts')

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse(
            'recipe:post_detail',
            args=[
                self.publish.year,
                self.publish.month,
                self.publish.day,
                self.slug
            ]
        )

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]

# Comment Model
class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [models.Index(fields=['created'])]

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'

class Rating(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='ratings'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    score = models.IntegerField()  # Rating score (e.g., 1-5)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'user')  # A user can rate a post only once

    def __str__(self):
        return f'Rating of {self.score} for {self.post.title} by {self.user.username}'
    