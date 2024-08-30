from django.db import models
from django.contrib.auth.models import User
import uuid
from datetime import datetime,date,time
from django.utils import timezone

# Create your models here.

class Profile(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    image = models.ImageField(upload_to="Profile_images",default="blank.webp")
    fname = models.CharField(max_length=100, blank=True)
    lname = models.CharField(max_length=100,blank=True)
    phone = models.IntegerField(blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=100,blank=True)
    country = models.CharField(max_length=100,blank=True)
    city = models.CharField(max_length=100,blank=True)

    def __str__(self):
        return self.user.username


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    file1 = models.FileField(upload_to="files")
    thumbnail = models.ImageField(default="",upload_to="Post_front_images")
    # image1 = models.ImageField(null=True,upload_to="Post_images")
    # image2 = models.ImageField(null=True,upload_to="Post_images")
    # image3 = models.ImageField(null=True,upload_to="Post_images")
    # day = models.CharField(blank=True,max_length=100)
    # day = models.CharField(max_length=100,default = timezone.now().day)
    text = models.TextField(max_length=500,default="")
    date = models.DateTimeField(default = datetime.now())
    title = models.CharField(max_length = 100)
    course = models.CharField(max_length = 100)
    subject = models.CharField(max_length = 100)
    no_of_likes = models.IntegerField(default = 0)
    profile = models.ForeignKey(Profile,on_delete = models.CASCADE)

    def __str__(self):
        return self.profile.user.username

class LikePost(models.Model):
    post_id = models.CharField(max_length =  500)
    username = models.CharField(max_length = 100)

    def __str__(self):
        return self.username