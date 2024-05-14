from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.utils.text import slugify


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'DRAFT'),
        ('published', 'PUBLISHED')
    )
    # id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique_for_date='publish', blank=True)
    content = models.TextField()
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='draft')
    publish = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-created',)

    def get_absolute_url(self):
        return reverse('post_details', args=[self.publish.year, self.publish.month, self.publish.day,
                                             self.slug])

    def save(
            self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        slug = slugify(self.title)
        self.slug = slug
        super().save(force_insert, force_update, using, update_fields)


# one instance = one row in the table
# one field = one column in the table
# one model = one table in the database
class Comment(models.Model):
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.content

    class Meta:
        ordering = ('-created',)
        indexes = [models.Index(fields=['created', 'active'])]
