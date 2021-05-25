import os

import requests
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from .models import Album, Track

# Headers for API calls
headers = {
    'x-rapidapi-key': os.getenv('X-RAPIDAPI-KEY'),
    'x-rapidapi-host': os.getenv('X-RAPIDAPI-HOST')
    }

# Create your views here.

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

class SignUp(CreateView):
    form_class = UserCreationForm
    success_url = '/'
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        super().form_valid(form)
        login(self.request, form.instance)
        return redirect(SignUp.success_url)

class AlbumList(LoginRequiredMixin, ListView):
    model = Album
    def get_queryset(self):
      return Album.objects.filter(user = self.request.user)

class AlbumDetail(LoginRequiredMixin, DetailView):
  model = Album

class AlbumAdd(LoginRequiredMixin, CreateView):
  model = Album
  fields = ['title', 'artist_name', 'genre', 'format']
  success_url = '/albums/'

  def form_valid(self, form):
    album_id = None
    form.instance.user = self.request.user
    album = form.save(commit=False) 
    url = "https://theaudiodb.p.rapidapi.com/searchalbum.php"

    querystring = {"s":form.instance.artist_name,"a":form.instance.title}
    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()
    
    if data['album'] != None:
      album_id = data['album'][0]['idAlbum']
      if 'strDescriptionEN' in data['album'][0].keys():
        album.description = data['album'][0]['strDescriptionEN']
      if 'strAlbum3DFace' in data['album'][0].keys():
        album.album_art_3d = data['album'][0]['strAlbum3DFace']
      if 'strAlbumThumbBack' in data['album'][0].keys():
        album.album_back_art = data['album'][0]['strAlbumThumbBack']
      if 'strAlbumThumb' in data['album'][0].keys():
        album.cover_art = data['album'][0]['strAlbumThumb']
      if 'strAlbumCDart' in data['album'][0].keys():
        album.cd_art = data['album'][0]['strAlbumCDart']
      if 'intYearReleased' in data['album'][0].keys():
        album.release_year = data['album'][0]['intYearReleased']
      
    album.save()
    if album_id:
      url = "https://theaudiodb.p.rapidapi.com/track.php"
      querystring = {"m":album_id}
      response = requests.get(url, headers=headers, params=querystring)
      data = response.json()
      tracks = data['track']
      for track in tracks:
        new_track = Track(name = track['strTrack'], track_no = int(track['intTrackNumber']), album = album)
        new_track.save()
    return super().form_valid(form)


class AlbumUpdate(LoginRequiredMixin, UpdateView):
  model = Album
  fields = ['title', 'artist_name', 'genre', 'format', 'description']


class AlbumDelete(LoginRequiredMixin, DeleteView):
  model=Album
  success_url = '/albums/'