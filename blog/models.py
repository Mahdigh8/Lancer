from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
# from django.contrib.auth.models import AbstractUser
# Create your models here.

# class User(AbstractUser):
# 	is_employer = models.BooleanField(default=False)
# 	is_worker = models.BooleanField(default=False)


class Worker(models.Model):
	user 		= models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='worker')
	tags 		= TaggableManager()
	def __str__(self):
		return self.user.username

	def get_absolute_url(self):
		return reverse('blog:profile', kwargs={'pk':self.user.id})



class PublishedManager(models.Manager):
	def get_queryset(self):
		return super(PublishedManager, self).get_queryset().filter(status='published')

class Post(models.Model):
	STATUS_CHOICES = (
			('draft', 'Draft'),
			('published', 'Published')
		)
	tags		= TaggableManager()
	user		= models.ForeignKey(User, on_delete=models.CASCADE)
	title		= models.CharField(max_length=200)
	body		= models.TextField()
	status 		= models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
	slug 		= models.SlugField(max_length=250, unique_for_date='publish')
	publish 	= models.DateTimeField(default=timezone.now)
	timestamp	= models.DateTimeField(auto_now_add=True)
	updated		= models.DateTimeField(auto_now=True)

	objects 	= models.Manager()
	published 	= PublishedManager()

	class Meta:
		ordering = ('-publish',)
	
	def get_absolute_url(self):
		return reverse('blog:post_detail', kwargs={'year':self.publish.year, 'slug':self.slug})

	def __str__(self):
		return self.title



class Comment(models.Model):
	post 		= models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
	name 		= models.CharField(max_length=200)
	body		= models.TextField()
	created 	= models.DateTimeField(auto_now_add=True)
	updated 	= models.DateTimeField(auto_now=True)
	active 		= models.BooleanField(default=True)

	class Meta:
		ordering = ('created',)

	def __str__(self):
		return 'Comment by {} on {}'.format(self.name, self.post)