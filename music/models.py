from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import FileExtensionValidator

# Create your models here.

class Category(models.Model):
    area = models.CharField(max_length=49)
    
    def __str__(self):
        return self.area
    
class Music(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=99)
    singer = models.CharField(max_length=299)
    description = models.TextField()
    duration = models.CharField(max_length=9, default='00:00:00')
    lyrics = models.TextField(blank=True, null=True)
    cover_picture = models.ImageField(upload_to='img/')
    audio = models.FileField(upload_to='aud/', validators=[FileExtensionValidator(allowed_extensions=['mp3','wav','aac','mp4','wma','flac','dsd','alac','3gpp'])])
    video = models.FileField(upload_to='vid/', blank=True, null=True, validators=[FileExtensionValidator(allowed_extensions=['mov','avi','mp4','webm','mkv','vbmv'])])
    release_date = models.DateTimeField(default=timezone.now)
    date = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    
    def __str__(self):
        return self.title

class Review(models.Model):
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    music = models.ForeignKey(Music, on_delete=models.CASCADE)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE, related_name='review_parent')

    class Meta:
        ordering=['-date']

    def __str__(self):
        return str(self.writer) + ' Review'

    @property
    def children(self):
        return Review.objects.filter(parent=self).reverse()

    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False

class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField()
    content = models.TextField()

    def __str__(self):
        return self.user
