from django.contrib.auth.models import User
from django.db import models

# Create your models here.

CHOICES = (
    ('1', 'Vinyl'),
    ('2', 'Compact Cassette'),
    ('3', '8-Track Tape'),
    ('4', 'Digital Audio Compact Disc'),
)

class Album(models.Model):
  title = models.CharField(max_length=100)
  artist_name = models.CharField('Artist Name', max_length=100)
  genre = models.CharField(max_length=50)
  description = models.TextField(blank=True, null=True)
  format = models.CharField(
    max_length=1,
    choices = CHOICES,
    default= CHOICES[3][0]
  )
  release_year = models.CharField(max_length=5, blank=True, null=True)
  cover_art= models.CharField(max_length=250, blank=True, null=True)
  cd_art = models.CharField(max_length=250, blank=True, null=True)
  album_art_3d = models.CharField(max_length=250, blank=True,null=True)
  album_back_art = models.CharField(max_length=250, blank=True,null=True)
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self):
    return f"Artist: {self.artist_name} Album: {self.title}"

class Track(models.Model):
  name = models.CharField(max_length=100)
  album = models.ForeignKey(Album, on_delete=models.CASCADE)
  track_no = models.IntegerField()

  def __str__(self):
    return f"{self.name} from {self.album.title}"
  class Meta:
    ordering = ['track_no']
 