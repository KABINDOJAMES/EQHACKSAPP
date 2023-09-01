from django.db import models
from django.shortcuts import reverse
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import User

# Create your models here.

#Posts model
class Post(models.Model):

    DRAFT = 'draft'
    PUBLISHED = 'published'

    STATUS = (
      (DRAFT, 'draft'),
      (PUBLISHED, 'published'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=230, unique=True)
    slug = models.CharField(max_length=300, unique=True)
    image_url = models.TextField(blank=True)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    alt = models.CharField(max_length=30)
    content = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS, default=DRAFT)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    keywords = models.TextField(blank=True)
    description = models.TextField(blank=True)
    views = models.IntegerField(default=0, null=True, blank=True)

    class Meta:
        ordering = ['-updated_on', '-created_on']
        verbose_name_plural = 'posts'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('posts-detail', args = [self.slug])

    @property
    def comment_count(self):
        return PostComment.objects.filter(post = self).count()
    

#Post Comments model  
class PostComment(models.Model):

    DRAFT = 'draft'
    PUBLISHED = 'published'

    STATUS = (
       (DRAFT, 'Waiting Approval'),
       (PUBLISHED, 'Approved'),
    )

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="postcomments")
    owner = models.CharField(max_length=20, null=False)
    body = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS, default=DRAFT)
    created_on = models.DateTimeField(auto_now_add=True)
    approved_on = models.DateTimeField(auto_now=True)
    reply = models.TextField(null=True, blank=True)
    reply_created_on = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-approved_on']

    def __str__(self):
        return self.body

class NewsArticle(models.Model):

    DRAFT = 'draft'
    PUBLISHED = 'published'

    STATUS = (
      (DRAFT, 'draft'),
      (PUBLISHED, 'published'),
    )

    title = models.CharField(max_length=230, unique=True)
    slug = models.CharField(max_length=300, unique=True)
    image_url = models.TextField(blank=True)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    alt = models.TextField(blank=True)
    content = models.TextField(blank=False)
    status = models.CharField(max_length=10, choices=STATUS, default=DRAFT)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    keywords = models.TextField(blank=True)
    description = models.TextField(blank=True)
    views = models.IntegerField(default=0, blank=True, null=True)
    
    class Meta:
        ordering = ['-updated_on', '-created_on']
        verbose_name_plural = 'News Articles'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news-detail', args = [self.slug])

    @property
    def comment_count(self):
        return NewsComment.objects.filter(newsarticle = self).count()

#news comments model
class NewsComment(models.Model):

    DRAFT = 'draft'
    PUBLISHED = 'published'

    STATUS = (
       (DRAFT, 'Waiting Approval'),
       (PUBLISHED, 'Approved'),
    )

    newsarticle = models.ForeignKey(NewsArticle, on_delete=models.CASCADE, related_name="newscomments")
    owner = models.CharField(max_length=20, null=False)
    body = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS, default=DRAFT)
    created_on = models.DateTimeField(auto_now_add=True)
    approved_on = models.DateTimeField(auto_now=True)
    reply = models.TextField(null=True, blank=True)
    reply_created_on = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-approved_on']

    def __str__(self):
        return self.body


#email subscription model
class SubscribedUsers(models.Model):
    email = models.CharField(unique=True, max_length=200)
    name = models.CharField(max_length=50)
    subscribe_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Subscribed users'

