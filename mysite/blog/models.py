from django.db import models
from django.utils import timezone
from users.models import Profile
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE) #many to one relationship
    liked = models.ManyToManyField(User, blank=True, related_name='likes')    
    def __str__(self):
        return self.title
    def num_likes(self):
        return self.liked.all().count()
    #tell django how to find url to any specific post
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
        
LIKE_CHOICES = (
    ('Like', 'Like'),
    ('Unlike', 'Unlike'),
)

class Like(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES, max_length=8)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

#this user liked which post? this table captures all instances of user liking a post
#class UserPostLikes(models.Model):
 #   user = models.ForeignKey(User, on_delete=models.CASCADE) 
 #   post_id = models.IntegerField()

    #TMRW FIGURE OUT HOW SO THAT WHEN YOU CLICK ON ARROW LIKE IT SENDS POST REQUEST TO:
    #POST/3/like




