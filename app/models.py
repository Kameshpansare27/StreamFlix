from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class CustomManager(models.Manager):
    def hollywood_list(self):
        return self.filter(category__exact="Hollywood")

    def anime_list(self):
        return self.filter(category__exact="Anime")

class Movie(models.Model):
    userid = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    movieid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=1000)
    description = models.TextField(blank=True, null=True)

    CATEGORY_CHOICES = (
        ("Hollywood", "Hollywood"),
        ("Anime", "Anime"),
    )
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='photos')  # Ensure this image exists
    video = models.FileField(upload_to="videos")
   
    objects = models.Manager()
    moviemanager = CustomManager()

    def __str__(self):
        return self.title


class Wishlist(models.Model):
    userid=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    movieid=models.ForeignKey(Movie,on_delete=models.CASCADE,null=True)
    qty=models.PositiveIntegerField(default=0)

    