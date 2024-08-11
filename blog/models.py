from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
#this is the models for each
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='blog_posts')
    def __str__(self):

        return self.title

    def get_absolute_url(self):
    	return reverse('post-detail', kwargs={'pk': self.pk})

    @property
    def likes_count(self):
        return self.like_set.count()

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'post')