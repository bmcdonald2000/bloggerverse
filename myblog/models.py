# django imports, packages and components
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField
from cloudinary.models import CloudinaryField
from datetime import datetime


# fields and behaviours for UserProfile model
class UserProfile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    Bio = models.TextField()
    profile_picture = CloudinaryField('image', blank=True, null=True,)
    Twitter = models.CharField(max_length=255, null=True, blank=True,)
    Instagram = models.CharField(max_length=255, null=True, blank=True,)
    Youtube = models.CharField(max_length=255, null=True, blank=True,)
    Linkedin = models.CharField(max_length=255, null=True, blank=True,)
    Website = models.CharField(max_length=255, null=True, blank=True,)
    Podcast = models.CharField(max_length=255, null=True, blank=True,)

    # function to identify the user
    def __str__(self):
        return str(self.user)

    # function to return to home page
    def get_absolute_url(self):
        return reverse('home')


# fields and behaviours for Post model
class Post(models.Model):
    title = models.CharField(max_length=255)
    # RichTextField gives user all the tool style their post
    image = CloudinaryField('image', blank=True, null=True,)
    body = RichTextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=70, default='law')
    summary = models.CharField(max_length=255)
    date = models.DateField(default=datetime.now)
    like = models.ManyToManyField(User, related_name='blog_post')

    # function for number of likes
    def num_likes(self):
        return self.like.count()

    # function for admin page to view post title and author
    def __str__(self):
        return self.title + ' | ' + str(self.author)

    # function to redirect user to the home page
    def get_absolute_url(self):
        return reverse('home')


# fields and behaviours for comment model
class comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments",
                             on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    # function to return data as string in the django admin
    def __str__(self):
        return '%s - %s' % (self.post.title, self.name)

    # redirects user to the post form if form successful
    def get_absolute_url(self):
        return reverse('details', args=[str(self.post.pk)])


# fields and behaviours for Category model
class Category(models.Model):
    # prevents duplicates
    name = models.CharField(max_length=70, unique=True)

    # categories are displayed in the admin section
    def __str__(self):
        return self.name

    # returns user to the add posts page so they can upload a post
    def get_absolute_url(self):
        return reverse('posts')

    # changes 'Categorys' to Categories in the admin section
    class Meta:
        verbose_name_plural = "Categories"
