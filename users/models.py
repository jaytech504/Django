from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from blog import models as blog_models
from PIL import Image
# Create your models here.
class Profile(models.Model):
  user = models.OneToOneField(User, on_delete= models.CASCADE)
  image = models.ImageField(default='default.jpg', upload_to='profile_pics')
  bio = models.CharField(max_length=100, blank=True)
  def __str__(self):
  	return f'{self.user.username} Profile'

  def save(self, *args, **kwargs):
  	super(Profile, self).save(*args, **kwargs)

  	img = Image.open(self.image.path)
  	if img.height > 300 or img.width > 300:
  		output_size = (300,300)
  		img.thumbnail(output_size)
  		img.save(self.image.path)

class Follow(models.Model):
	follower = models.ForeignKey(User, related_name="following", on_delete=models.CASCADE)
	followed = models.ForeignKey(User, related_name="followers", on_delete=models.CASCADE)
	created_at = models.DateTimeField(default=timezone.now)

	class Meta:
		unique_together = ('follower', 'followed')

	def __str__(self):
		return f"{self.follower} follows {self.followed}" 

class Notification(models.Model):
	NOTIFICATION_TYPES = (
		('like', 'Like'),
		('follow', 'Follow'),
	)
	recipient = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
	sender = models.ForeignKey(User, related_name='sender_notifications', on_delete=models.CASCADE)
	notification_type = models.CharField(choices=NOTIFICATION_TYPES, max_length=10)
	post = models.ForeignKey(blog_models.Post, null=True, blank=True, on_delete=models.CASCADE)
	timestamp = models.DateTimeField(default=timezone.now)
	is_read = models.BooleanField(default=False)

	def __str__(self):
		return f"{self.sender} {self.notification_type} {self.recipient}"