from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):
    STATUS_CHOICES = (
            ('draft', 'Draft'),
            ('published', 'Published'),
            )
    title = models.CharField(max_length=250)
    # fancy name URLs
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    # ForeignKey many-to-one CASCADE al borrar el author borra sus posts
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    body = models.TextField()
    publish = models.DateField(default=timezone.now)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    class Meta:
        ordering = ('-publish',)
    def __str__(self):
        return self.title
