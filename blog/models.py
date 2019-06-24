from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from taggit.managers import TaggableManager
from froala_editor.fields import FroalaField
# Create your models here.
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,self).get_queryset().filter(status="publish")
class Post(models.Model):
    objects=models.Manager()
    published=PublishedManager()
    tags=TaggableManager()
    STATUS_CHOICES=(('draft','Draft'),('publish','Publish'))
    title=models.CharField(max_length=250)
    #image=models.ImageField(upload_to='images/')
    slug=models.SlugField(max_length=250,unique=True)
    author=models.ForeignKey(User,on_delete=models.CASCADE,related_name='blog_posts')
    body=FroalaField()
    publish=models.DateTimeField(default=timezone.now)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    status=models.CharField(max_length=10,choices=STATUS_CHOICES,default='draft')
    def get_absolute_url(self):
        return reverse('blog:post_details',
                      args=[self.slug ])

    class Meta:
        ordering=('-publish',)
    def __str__(self):
        return self.title

''' comment class for comment on post'''
class Comment(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    name=models.CharField(max_length=250)
    email=models.EmailField()
    body=models.TextField()
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    active=models.BooleanField(default=True)
    class Meta:
        ordering =('created',)
    def __str__(self):
        return 'comment by {} on {}'.format(self.name,self.post)
