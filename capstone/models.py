from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime
from django.utils import timezone

class User(AbstractUser):
    pass
class Magazine(models.Model):
    title = models.CharField(max_length=100)
    five_star_count = models.IntegerField(default=5)
    def __str__(self):
        return f"({self.title}, {self.five_star_count})"

class Tag(models.Model):
    id=models.AutoField(primary_key=True)
    tag_name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return f"{self.id}, {self.tag_name}"

class Article(models.Model):
    article_by = models.ForeignKey("User", on_delete=models.CASCADE, related_name="article_user")
    title= models.CharField(max_length=100, unique=True)
    synopsis= models.CharField(max_length=2000)
    content= models.CharField(max_length=20000)
    publish_date = models.DateTimeField(default=timezone.now)
    read_count = models.IntegerField(default=0)
    article_picture = models.CharField(max_length=10000,default='')
    article_column = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.title}, {self.article_by} ({self.synopsis}, {self.publish_date}, {self.content}, {self.read_count}, {self.article_picture}), {self.article_column}"

class Articletotag(models.Model):
    tag_obj = models.ForeignKey("Tag", on_delete=models.CASCADE, related_name="tag_related")
    article_obj = models.ForeignKey("Article", on_delete=models.CASCADE, related_name="article_related")

    def __str__(self):
        return f"{self.tag_obj} {self.article_obj}"
